# Generated by Django 4.2.3 on 2023-10-20 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivedstudent',
            name='student_lrn',
        ),
        migrations.RemoveField(
            model_name='student',
            name='student_lrn',
        ),
        migrations.AddField(
            model_name='archivedstudent',
            name='student_school_id',
            field=models.CharField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='student',
            name='student_school_id',
            field=models.CharField(null=True, unique=True),
        ),
    ]