# Generated by Django 4.2.3 on 2023-10-25 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0014_studentanswer_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentanswer',
            name='assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answer', to='assessment.assessmentsession'),
        ),
    ]