# Generated by Django 4.2.3 on 2023-10-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_app', '0014_alter_admin_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='has_ongoing_assessment',
            field=models.BooleanField(default=False),
        ),
    ]