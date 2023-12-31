# Generated by Django 4.2.3 on 2023-11-22 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0005_teacher_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_code', models.PositiveIntegerField()),
                ('registration_code', models.PositiveBigIntegerField()),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='teacher',
            name='grade_level',
            field=models.IntegerField(choices=[(4, 'Grade 4'), (5, 'Grade 5'), (6, 'Grade 6')]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='section',
            field=models.CharField(choices=[('Rizal', 'Rizal'), ('Bonifacio', 'Bonifacio'), ('Aguinaldo', 'Aguinaldo'), ('Luna', 'Luna'), ('Mabini', 'Mabini'), ('Marcos', 'Marcos'), ('Duterte', 'Duterte'), ('Macapagal', 'Macapagal'), ('Roxas', 'Roxas'), ('Garcia', 'Garcia'), ('Pluto', 'Pluto'), ('Earth', 'Earth'), ('Venus', 'Venus'), ('Jupiter', 'Jupiter')]),
        ),
    ]
