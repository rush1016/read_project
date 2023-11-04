# Generated by Django 4.2.3 on 2023-11-02 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_question_question_type'),
        ('assessment', '0018_remove_screeningassessment_number_of_questions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmentsessionpassage',
            name='passage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_passage', to='materials.passage'),
        ),
    ]
