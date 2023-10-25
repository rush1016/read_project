# Generated by Django 4.2.3 on 2023-10-23 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_rename_has_ongoing_assessment_student_is_screened'),
        ('assessment', '0006_alter_assessmentsession_assessment_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmentsession',
            name='student',
            field=models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
    ]