# Generated by Django 4.2.3 on 2023-09-26 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='class_section',
            field=models.CharField(default='undefined', max_length=80),
        ),
    ]
