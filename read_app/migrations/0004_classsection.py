# Generated by Django 4.2.3 on 2023-11-22 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0003_teacher_grade_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_level', models.IntegerField()),
                ('section_name', models.CharField(max_length=80)),
            ],
        ),
    ]