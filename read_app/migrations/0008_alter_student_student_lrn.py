# Generated by Django 4.2.3 on 2023-10-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0007_student_student_lrn_alter_question_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_lrn',
            field=models.FloatField(null=True, unique=True),
        ),
    ]