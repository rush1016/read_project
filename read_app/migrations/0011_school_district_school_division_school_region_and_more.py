# Generated by Django 4.2.3 on 2023-11-22 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0010_admin_school_alter_teacher_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='district',
            field=models.CharField(default='Division of Angeles City', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='division',
            field=models.CharField(default='Division of Angeles City', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='region',
            field=models.CharField(default='Region III', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='admin',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school', to='read_app.school'),
        ),
    ]
