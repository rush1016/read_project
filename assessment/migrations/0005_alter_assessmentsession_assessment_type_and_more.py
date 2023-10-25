# Generated by Django 4.2.3 on 2023-10-22 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0004_studentanswer_assessment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmentsession',
            name='assessment_type',
            field=models.CharField(choices=[('Screening', 'Screening'), ('Normal', 'Normal')], max_length=16),
        ),
        migrations.AlterField(
            model_name='studentanswer',
            name='answer_content',
            field=models.CharField(max_length=512),
        ),
    ]