from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, PostReply, Subscribers


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    subs = Subscribers.objects.filter(category=instance.category)

    subject = f'New post in category {instance.category}'

    text_content = (
        f'Post: {instance.title}\n'
        f'Link: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Post: {instance.title}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Link</a>'
    )
    for sub in subs:
        msg = EmailMultiAlternatives(subject, text_content, None, [sub.user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=PostReply)
def reply_created(instance, created, **kwargs):
    if not created:
        return

    email = instance.announce.author.email

    subject = f'User {instance.user} replied to your post.'

    text_content = (
        f'User {instance.user} replied to your post.'
        f'Post: {instance.announce.title}\n'
        f'link to the replies page: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'User {instance.user} replied to your post.'
        f'Post: {instance.announce.title}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'link to the replies page</a>'
    )
    msg = EmailMultiAlternatives(subject, text_content, None, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=PostReply)
def reply_created(instance, created, **kwargs):
    if created:
        return

    if instance.submit_reply:
        email = instance.user.email

        subject = f'Post author {instance.announce.author} submit your reply.'

        text_content = (
            f'Post author {instance.announce.author} submit your reply.'
            f'Post: {instance.announce.title}\n'
            f'Link: http://127.0.0.1:8000{instance.announce.get_absolute_url()}'
        )
        html_content = (
            f'Post author {instance.announce.author} submit your reply.'
            f'Post: {instance.announce.title}<br>'
            f'<a href="http://127.0.0.1{instance.announce.get_absolute_url()}">'
            f'Link</a>'
        )
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
