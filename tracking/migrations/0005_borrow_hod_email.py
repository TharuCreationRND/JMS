# Generated by Django 5.2.3 on 2025-06-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_breakdown_created_by_alter_job_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='hod_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
