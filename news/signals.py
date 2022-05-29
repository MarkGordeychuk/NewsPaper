from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site

from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def send_mail_to_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add' and isinstance(instance, Post):
        for user in User.objects.filter(categories_subscribed__post=instance).distinct():
            html_content = render_to_string(
                'mail_post_create.html',
                {
                    'user': user,
                    'post': instance,
                    'site': Site.objects.get_current(),
                }
            )
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=f'Здравствуй, {user}. Новая статья в твоём любимом разделе!',
                from_email='winvat@yandex.ru',
                to=(user.email,),
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
