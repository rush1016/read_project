# Generated by Django 4.2.3 on 2023-10-18 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0018_screeningtestpreset'),
    ]

    operations = [
        migrations.AddField(
            model_name='passage',
            name='passage_length',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
