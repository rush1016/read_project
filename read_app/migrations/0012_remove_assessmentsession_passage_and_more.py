# Generated by Django 4.2.3 on 2023-10-18 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0011_alter_student_assessments_done_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessmentsession',
            name='passage',
        ),
        migrations.AddField(
            model_name='assessmentsession',
            name='assessment_type',
            field=models.CharField(choices=[('Screening', 'Screening'), ('Normal', 'Normal')], default='Normal', max_length=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AssessmentSessionPassage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('assessment_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read_app.assessmentsession')),
                ('passage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read_app.passage')),
            ],
        ),
    ]
