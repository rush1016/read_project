# Generated by Django 4.2.3 on 2023-10-23 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_assessmentpreset_passage_preset'),
        ('assessment', '0010_delete_assessmentpreset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentanswer',
            name='answer_content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.choice'),
        ),
    ]
