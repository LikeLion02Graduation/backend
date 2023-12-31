# Generated by Django 3.2.8 on 2024-01-06 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagname', models.CharField(max_length=100)),
                ('enable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=20)),
                ('img', models.TextField()),
                ('description', models.TextField()),
                ('buyers', models.ManyToManyField(blank=True, related_name='buyers', to=settings.AUTH_USER_MODEL)),
                ('hashtag', models.ManyToManyField(blank=True, related_name='map_hashtag', to='map.Hashtag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='map_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('link', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('hashtag', models.ManyToManyField(blank=True, related_name='recom_hashtag', to='map.Hashtag')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recom_map', to='map.map')),
                ('place', models.ManyToManyField(related_name='recom_place', to='map.Place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recom_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='React',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('emoji', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('content', models.TextField()),
                ('recommend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='react_recom', to='map.recommend')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='react_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(max_length=10, null=True)),
                ('recommend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alert_recom', to='map.recommend')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alert_user', to=settings.AUTH_USER_MODEL)),
                ('viewuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
