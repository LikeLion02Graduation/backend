# Generated by Django 3.2.8 on 2024-01-08 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='img',
            field=models.TextField(blank=True, null=True),
        ),
    ]