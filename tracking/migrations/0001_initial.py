# Generated by Django 5.2.3 on 2025-06-20 07:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_date', models.DateField()),
                ('center', models.CharField(max_length=100)),
                ('area_manager', models.CharField(max_length=100)),
                ('area_manager_email', models.EmailField(max_length=254)),
                ('job_number', models.CharField(max_length=50, unique=True)),
                ('item_type', models.CharField(max_length=100)),
                ('request_by', models.CharField(max_length=100)),
                ('requester_designation', models.CharField(max_length=100)),
                ('job_assignee', models.CharField(max_length=100)),
                ('center_sent_date', models.DateField()),
                ('head_office_receive_date', models.DateField()),
                ('serial_number', models.CharField(max_length=100)),
                ('pronto_no_receive', models.CharField(max_length=100)),
                ('pronto_no_sent', models.CharField(max_length=100)),
                ('head_office_sent_date', models.DateField()),
                ('center_receive_date', models.DateField()),
                ('finish_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Finished', 'Finished'), ('Rejected', 'Rejected'), ('Purchase', 'Item in Purchase')], max_length=20)),
                ('remark', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
