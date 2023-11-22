# Generated by Django 4.2.3 on 2023-11-22 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0009_alter_school_registration_code'),
        ('students', '0002_delete_classsection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_school_id',
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='read_app.school'),
        ),
    ]
