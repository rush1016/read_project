# Generated by Django 4.2.3 on 2023-10-01 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0005_archivedstudent_student_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]