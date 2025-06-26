import ssl
ssl._create_default_https_context = ssl._create_unverified_context


import asyncio
from datetime import datetime, date

import httpx
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
from telegram.request import HTTPXRequest

from asgiref.sync import sync_to_async
from django.utils.timezone import localtime
from django.contrib.auth import authenticate

from tracking.models import Job, Breakdown, Borrow

user_states = {}
authenticated_users = {}
temp_usernames = {}

ITEM_TYPES = ["Mobile", "Projector"]

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_states[chat_id] = "awaiting_username"
    await update.message.reply_text("Welcome! Please enter your username to login:", reply_markup=ReplyKeyboardRemove())


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    if chat_id not in authenticated_users:
        state = user_states.get(chat_id)

        if state == "awaiting_username":
            temp_usernames[chat_id] = text
            user_states[chat_id] = "awaiting_password"
            await update.message.reply_text("Please enter your password:")
            return

        elif state == "awaiting_password":
            username = temp_usernames.get(chat_id)
            password = text
            user = await sync_to_async(authenticate)(username=username, password=password)

            if user:
                authenticated_users[chat_id] = username
                user_states[chat_id] = "waiting_for_option"
                temp_usernames.pop(chat_id, None)
                await update.message.reply_text(
                    f"✅ Welcome, *{username}*! You are now logged in.\n\n"
                    "Please choose an option:\n"
                    "1. Job Report\n"
                    "2. Job Breakdown Report\n"
                    "3. Borrower Report\n\n"
                    "Send the number of your choice.",
                    parse_mode='Markdown'
                )
            else:
                user_states[chat_id] = "awaiting_username"
                temp_usernames.pop(chat_id, None)
                await update.message.reply_text(
                    "❌ Invalid username or password. Try again.\n\nEnter your username:"
                )
            return

        else:
            user_states[chat_id] = "awaiting_username"
            await update.message.reply_text("Please login first.\nEnter your username:")
            return

    # Authenticated user
    state = user_states.get(chat_id, "waiting_for_option")

    if text == "/logout":
        authenticated_users.pop(chat_id, None)
        user_states[chat_id] = "awaiting_username"
        temp_usernames.pop(chat_id, None)
        await update.message.reply_text("You have been logged out. Please login again.\nEnter your username:")
        return

    if state == "waiting_for_option":
        if text == "1":
            user_states[chat_id] = "waiting_for_job_number_for_report"
            await update.message.reply_text("Please enter the job number for Job Report:")
        elif text == "2":
            user_states[chat_id] = "waiting_for_job_number_for_breakdown"
            await update.message.reply_text("Please enter the job number for Breakdown Report:")
        elif text == "3":
            user_states[chat_id] = "waiting_for_item_type_for_borrow"
            keyboard = [[item] for item in ITEM_TYPES]
            await update.message.reply_text("Please select the Item Type for Borrower Report:",
                                            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        else:
            await update.message.reply_text("Invalid option. Please enter 1, 2, or 3.")
    elif state == "waiting_for_job_number_for_report":
        reply = await get_job_report(text)
        await update.message.reply_text(reply, parse_mode='Markdown')
        user_states[chat_id] = "waiting_for_option"
        await start_menu_again(update, context)

    elif state == "waiting_for_job_number_for_breakdown":
        reply = await get_breakdown_report(text)
        await update.message.reply_text(reply, parse_mode='Markdown')
        user_states[chat_id] = "waiting_for_option"
        await start_menu_again(update, context)

    elif state == "waiting_for_item_type_for_borrow":
        if text not in ITEM_TYPES:
            await update.message.reply_text("Invalid item type selected. Please choose from the keyboard.")
            return

        reply = await get_borrow_report_by_item(text)
        await update.message.reply_text(reply, parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
        user_states[chat_id] = "waiting_for_option"
        await start_menu_again(update, context)

    else:
        await update.message.reply_text("Send /start to begin.", reply_markup=ReplyKeyboardRemove())


async def start_menu_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please choose an option:\n"
        "1. Job Report\n"
        "2. Job Breakdown Report\n"
        "3. Borrower Report\n\n"
        "Send the number of your choice.",
        reply_markup=ReplyKeyboardRemove()
    )

# Data formatting
def _format_date(value):
    if not value:
        return "N/A"
    if isinstance(value, datetime):
        return localtime(value).strftime("%Y-%m-%d %H:%M")
    elif isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return str(value)

# Report functions
@sync_to_async
def get_job_report(job_number):
    job = Job.objects.filter(job_number__iexact=job_number).first()
    if not job:
        return f"❌ No job found for job number: {job_number}"

    return (
        f"📋 *Job Report* — *{job.job_number}*\n\n"
        f"────────────────────────────\n"
        f"📅 Date: {_format_date(job.job_date)}\n"
        f"🏢 Center: {job.center or 'N/A'}\n"
        f"👤 Area Manager: {job.area_manager or 'N/A'} ({job.area_manager_email or 'N/A'})\n"
        f"🔧 Item Type: {job.item_type or 'N/A'}\n"
        f"👥 Request By: {job.request_by or 'N/A'} ({job.requester_designation or 'N/A'})\n"
        f"🧑‍🔧 Job Assignee: {job.job_assignee or 'N/A'}\n"
        f"📤 Center Sent Date: {_format_date(job.center_sent_date)}\n"
        f"📥 HO Received Date: {_format_date(job.head_office_receive_date)}\n"
        f"🔢 Serial Number: {job.serial_number or 'N/A'}\n"
        f"📦 Pronto No Receive: {job.pronto_no_receive or 'N/A'}\n"
        f"📤 Pronto No Sent: {job.pronto_no_sent or 'N/A'}\n"
        f"📤 HO Sent Date: {_format_date(job.head_office_sent_date)}\n"
        f"📥 Center Receive Date: {_format_date(job.center_receive_date)}\n"
        f"✅ Finish Date: {_format_date(job.finish_date)}\n"
        f"📊 Status: {job.status or 'N/A'}\n"
        f"📝 Remark: {job.remark or 'None'}\n"
        f"👤 Created By: {job.created_by or 'N/A'}\n"
        f"────────────────────────────"
    )


@sync_to_async
def get_breakdown_report(job_number):
    breakdowns = Breakdown.objects.filter(job_number__iexact=job_number)
    if not breakdowns.exists():
        return f"❌ No breakdown reports found for job number: {job_number}"

    reply = f"🔧 *Breakdown Report* — Job {job_number}\n────────────────────────────\n"
    for b in breakdowns:
        reply += (
            f"📅 Date: {_format_date(b.date)}\n"
            f"🏢 Center: {b.center or 'N/A'}\n"
            f"⚠️ Issue: {b.issue or 'N/A'}\n"
            f"🧑‍🔧 Job Assignee: {b.job_assignee or 'N/A'}\n"
            f"💬 Comment: {b.comment or 'None'}\n"
            f"────────────────────────────\n\n"
        )
    return reply


@sync_to_async
def get_borrow_report_by_item(item_name):
    borrows = Borrow.objects.filter(item_type__iexact=item_name)
    if not borrows.exists():
        return f"❌ No borrow reports found for item: {item_name}"

    reply = f"📦 *Borrower Report* — Item: {item_name}\n────────────────────────────\n\n"
    for b in borrows:
        reply += (
            f"📅 Date: {_format_date(b.date)}\n"
            f"👤 Name: {b.name or 'N/A'} | {b.designation or 'N/A'} | {b.department or 'N/A'}\n"
            f"📦 Item Type: {b.item_type or 'N/A'} for {b.days or 'N/A'} days\n"
            f"📧 Email: {b.email or 'N/A'}\n"
            f"📝 Reason: {b.reason or 'None'}\n"
            f"👔 HOD Email: {b.hod_email or 'N/A'}\n"
            f"👤 Created By: {b.created_by or 'N/A'}\n"
            f"────────────────────────────\n\n"
        )
    return reply

# Main bot runner
async def run_bot():
    TOKEN = "8158821371:AAGfaEV2B8j26moJgQseNyghqHubfvp6dTo"


    request = HTTPXRequest()

    app = ApplicationBuilder().token(TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("logout", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Telegram bot running...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        print("Stopping bot...")
    finally:
        await app.updater.stop_polling()
        await app.stop()
        await app.shutdown()
        await client.aclose()
