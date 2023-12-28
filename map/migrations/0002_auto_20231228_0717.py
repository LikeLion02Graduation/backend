# Generated by Django 3.2.8 on 2023-12-27 22:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='buyers',
            field=models.ManyToManyField(blank=True, related_name='buyers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='map',
            name='hashtag',
            field=models.ManyToManyField(blank=True, related_name='map_hashtag', to='map.Hashtag'),
        ),
        migrations.AlterField(
            model_name='recommend',
            name='hashtag',
            field=models.ManyToManyField(blank=True, related_name='recom_hashtag', to='map.Hashtag'),
        ),
    ]