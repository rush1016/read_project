# Generated by Django 4.2.3 on 2023-10-25 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0004_rename_has_ongoing_assessment_student_is_screened'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='student_instance', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
