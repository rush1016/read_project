# Generated by Django 4.2.3 on 2023-11-20 20:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment_type', models.CharField(choices=[('Screening', 'Screening'), ('Graded', 'Graded')], max_length=16)),
                ('number_of_questions', models.IntegerField(default=0)),
                ('grade_level', models.IntegerField()),
                ('total_score', models.IntegerField(blank=True, null=True)),
                ('total_reading_time', models.PositiveIntegerField(blank=True, null=True)),
                ('total_answering_time', models.PositiveIntegerField(blank=True, null=True)),
                ('assigned_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('passcode', models.CharField(max_length=16, unique=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_session', to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField(default=False)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.choice')),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answer', to='assessment.assessmentsession')),
                ('passage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.passage')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='ScreeningAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_passage', models.IntegerField(default=1)),
                ('correct_literal', models.PositiveIntegerField(default=0)),
                ('correct_inferential', models.PositiveIntegerField(default=0)),
                ('correct_critical', models.PositiveIntegerField(default=0)),
                ('total_literal', models.PositiveIntegerField(default=0)),
                ('total_inferential', models.PositiveIntegerField(default=0)),
                ('total_critical', models.PositiveIntegerField(default=0)),
                ('assessment_session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='screening_assessment', to='assessment.assessmentsession')),
            ],
        ),
        migrations.CreateModel(
            name='GradedAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oral_reading_score', models.FloatField(blank=True, null=True)),
                ('reading_comprehension_score', models.FloatField(blank=True, null=True)),
                ('oral_reading_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('reading_comprehension_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('overall_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('reading_speed', models.FloatField(blank=True, null=True)),
                ('assessment_session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='graded_assessment', to='assessment.assessmentsession')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentSessionPassage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(null=True)),
                ('score', models.PositiveIntegerField(blank=True, null=True)),
                ('reading_time', models.PositiveIntegerField(blank=True, null=True)),
                ('answering_time', models.PositiveIntegerField(blank=True, null=True)),
                ('assessment_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_passage', to='assessment.assessmentsession')),
                ('passage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_passage', to='materials.passage')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentMiscue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=64)),
                ('miscue', models.CharField(choices=[('Mispronunciation', 'Mispronunciation'), ('Omission', 'Omission'), ('Substitution', 'Substitution'), ('Insertion', 'Insertion'), ('Repetition', 'Repetition'), ('Transposition', 'Transposition'), ('Reversal', 'Reversal'), ('Self-correction', 'Self-correction')])),
                ('index', models.IntegerField()),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oral_miscues', to='assessment.assessmentsession')),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.passage')),
            ],
        ),
    ]
