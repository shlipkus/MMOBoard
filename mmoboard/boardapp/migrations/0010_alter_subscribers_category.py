# Generated by Django 5.0.6 on 2024-05-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0009_subscribers_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='category',
            field=models.CharField(default='Tanks', max_length=128, unique=True),
        ),
    ]
