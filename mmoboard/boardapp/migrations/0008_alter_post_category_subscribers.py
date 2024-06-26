# Generated by Django 5.0.6 on 2024-05-20 08:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0007_rename_announcement_post_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Tanks', 'Tanks'), ('Healers', 'Healers'), ('Damage Dealer', 'Damagedealer'), ('Merchants', 'Merchants'), ('Guild Masters', 'Guildmasters'), ('Quest Givers', 'Questgivers'), ('Blacksmiths', 'Blacksmiths'), ('Tanners', 'Tanners'), ('Potion Makers', 'Potionmakers'), ('Spell Masters', 'Spellmasters')], default='Tanks', max_length=128),
        ),
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
