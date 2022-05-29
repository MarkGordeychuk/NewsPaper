import logging
import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from news.models import Post

logger = logging.getLogger(__name__)


def my_job():
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


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="tue", hour="23", minute="56"
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")