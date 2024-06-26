# Generated by Django 5.0.6 on 2024-05-20 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0008_alter_post_category_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribers',
            name='category',
            field=models.CharField(choices=[('Tanks', 'Tanks'), ('Healers', 'Healers'), ('Damage Dealer', 'Damagedealer'), ('Merchants', 'Merchants'), ('Guild Masters', 'Guildmasters'), ('Quest Givers', 'Questgivers'), ('Blacksmiths', 'Blacksmiths'), ('Tanners', 'Tanners'), ('Potion Makers', 'Potionmakers'), ('Spell Masters', 'Spellmasters')], default='Tanks', max_length=128),
        ),
    ]
