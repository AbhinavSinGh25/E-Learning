# Generated by Django 4.1 on 2023-03-18 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0009_quiz_q_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='q_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='q_time',
            field=models.IntegerField(default=0),
        ),
    ]
