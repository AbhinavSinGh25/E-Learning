# Generated by Django 4.1b1 on 2023-03-18 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0003_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='q_score',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='q_time',
            field=models.IntegerField(),
        ),
    ]
