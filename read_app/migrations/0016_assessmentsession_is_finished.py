# Generated by Django 4.2.3 on 2023-10-18 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0015_student_has_ongoing_assessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentsession',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
