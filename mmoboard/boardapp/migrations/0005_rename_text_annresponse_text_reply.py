# Generated by Django 5.0.6 on 2024-05-17 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0004_annresponse_time_in'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annresponse',
            old_name='text',
            new_name='text_reply',
        ),
    ]
