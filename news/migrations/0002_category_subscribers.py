# Generated by Django 4.0.3 on 2022-05-09 23:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='categories_subscribed', to=settings.AUTH_USER_MODEL),
        ),
    ]