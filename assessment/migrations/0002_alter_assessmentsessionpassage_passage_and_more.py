# Generated by Django 4.2.3 on 2023-10-19 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0020_remove_assessmentsessionpassage_assessment_session_and_more'),
        ('materials', '0001_initial'),
        ('assessment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmentsessionpassage',
            name='passage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.passage'),
        ),
        migrations.AlterField(
            model_name='screeningtestpreset',
            name='passages',
            field=models.ManyToManyField(to='materials.passage'),
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_content', models.CharField(max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read_app.student')),
            ],
        ),
    ]