import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from news.models import Post


@shared_task
def weekly_newsletter_every_monday_8am():
    week = datetime.date.today().isocalendar()[1]
    if datetime.date.today().weekday() < 5:
        week -= 1
    for user in User.objects.exclude(categories_subscribed=None):
        posts = Post.objects.filter(category__subscribers=user, date_in__week=week).distinct()
        html_content = render_to_string(
            'weekly_newsletter.html',
            {
                'user': user,
                'posts': posts,
                'site': Site.objects.get_current(),
            }
        )
        msg = EmailMultiAlternatives(
            subject='Еженедельная рассылка',
            body='Новости за прошедшую неделю:',
            from_email='winvat@yandex.ru',
            to=(user.email,),
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
