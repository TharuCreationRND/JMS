from django.core.management.base import BaseCommand
import asyncio
from tracking.telegram_bot import run_bot

class Command(BaseCommand):
    help = "Run the Telegram bot"

    def handle(self, *args, **options):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # No current event loop in this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If the loop is already running (e.g., in some environments like Jupyter),
            # run coroutine differently
            import nest_asyncio
            nest_asyncio.apply()
            loop.run_until_complete(run_bot())
        else:
            loop.run_until_complete(run_bot())
