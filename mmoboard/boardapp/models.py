from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    class Category(models.TextChoices):
        Tanks = 'Tanks',
        Healers = 'Healers',
        DamageDealer = 'Damage Dealer',
        Merchants = 'Merchants',
        GuildMasters = 'Guild Masters',
        QuestGivers = 'Quest Givers',
        Blacksmiths = 'Blacksmiths',
        Tanners = 'Tanners',
        PotionMakers = 'Potion Makers',
        SpellMasters = 'Spell Masters',

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=128, choices=Category, default='Tanks')
    title = models.CharField(max_length=128)
    text = models.TextField(default='Your text')

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.pk)])

    def __str__(self):
        return self.title


class PostReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announce = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    text_reply = models.TextField(default='Your response')
    submit_reply = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('prof')


class VerifyUser(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.EmailField(default='example@mail.com')
    confirm_code = models.CharField(max_length=6)


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/', null=True, max_length=255)


class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video/', null=True, max_length=255)


class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=128, default='Tanks', unique=True)
