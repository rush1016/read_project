# Generated by Django 4.2.3 on 2023-10-04 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0002_alter_student_student_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='teacher_code',
            field=models.CharField(default=123456, max_length=80),
            preserve_default=False,
        ),
    ]
