# Generated by Django 5.0.6 on 2024-05-17 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0005_rename_text_annresponse_text_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='annresponse',
            name='submit_reply',
            field=models.BooleanField(default=False),
        ),
    ]
