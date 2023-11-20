# Generated by Django 4.2.3 on 2023-11-20 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_school_id', models.CharField(blank=True, null=True, unique=True)),
                ('first_name', models.CharField(max_length=80)),
                ('middle_name', models.CharField(blank=True, null=True)),
                ('last_name', models.CharField(max_length=80)),
                ('suffix', models.CharField(blank=True, choices=[('Sr.', 'Sr.'), ('Jr.', 'Jr.'), ('III', 'III')], null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('grade_level', models.IntegerField()),
                ('class_section', models.CharField(max_length=80)),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
                ('is_screened', models.BooleanField(default=False)),
                ('screening', models.BooleanField(default=False)),
                ('gst_score', models.PositiveIntegerField(blank=True, null=True)),
                ('recommended_grade_level', models.PositiveIntegerField(default=0)),
                ('overall_rating', models.CharField(default='Not yet screened', max_length=64)),
                ('words_per_minute', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('mean_read_time', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('mean_score', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('assessments_done', models.IntegerField(default=0)),
                ('first_grade_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration'), ('Passed Screening Test', 'Passed Screening Test'), ('Further Assessment Required', 'Further Assessment Required'), ('Not yet screened', 'Not yet screened')], null=True)),
                ('second_grade_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration'), ('Passed Screening Test', 'Passed Screening Test'), ('Further Assessment Required', 'Further Assessment Required'), ('Not yet screened', 'Not yet screened')], null=True)),
                ('third_grade_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration'), ('Passed Screening Test', 'Passed Screening Test'), ('Further Assessment Required', 'Further Assessment Required'), ('Not yet screened', 'Not yet screened')], null=True)),
                ('fourth_grade_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration'), ('Passed Screening Test', 'Passed Screening Test'), ('Further Assessment Required', 'Further Assessment Required'), ('Not yet screened', 'Not yet screened')], null=True)),
                ('fifth_grade_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration'), ('Passed Screening Test', 'Passed Screening Test'), ('Further Assessment Required', 'Further Assessment Required'), ('Not yet screened', 'Not yet screened')], null=True)),
                ('sixth_grade_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration'), ('Passed Screening Test', 'Passed Screening Test'), ('Further Assessment Required', 'Further Assessment Required'), ('Not yet screened', 'Not yet screened')], null=True)),
                ('seventh_grade_rating', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration'), ('Passed Screening Test', 'Passed Screening Test'), ('Further Assessment Required', 'Further Assessment Required'), ('Not yet screened', 'Not yet screened')], null=True)),
                ('teacher', models.ForeignKey(limit_choices_to={'is_teacher': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english_rating', models.CharField(blank=True, null=True)),
                ('english_recommended_grade', models.IntegerField(blank=True, null=True)),
                ('english_gst_score', models.PositiveIntegerField(blank=True, null=True)),
                ('filipino_rating', models.CharField(blank=True, null=True)),
                ('filipino_recommended_grade', models.IntegerField(blank=True, null=True)),
                ('filipino_gst_score', models.PositiveIntegerField(blank=True, null=True)),
                ('first_grade_eng', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('second_grade_eng', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('third_grade_eng', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('fourth_grade_eng', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('fifth_grade_eng', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('sixth_grade_eng', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('seventh_grade_eng', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('first_grade_fil', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('second_grade_fil', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('third_grade_fil', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('fourth_grade_fil', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('fifth_grade_fil', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('sixth_grade_fil', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('seventh_grade_fil', models.CharField(blank=True, choices=[('Independent', 'Independent'), ('Instructional', 'Instructional'), ('Frustration', 'Frustration')], null=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_rating', to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='ArchivedStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('student_id', models.IntegerField()),
                ('student_school_id', models.CharField(null=True, unique=True)),
                ('grade_level', models.IntegerField()),
                ('class_section', models.CharField(max_length=80)),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
                ('is_approved', models.BooleanField(default=False)),
                ('date_archived', models.DateField(auto_now_add=True)),
                ('previous_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
