# Generated by Django 5.0.2 on 2025-03-18 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobboardresult',
            name='salary',
            field=models.CharField(default='', max_length=100),
        ),
    ]
