# Generated by Django 4.1b1 on 2023-03-18 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0005_alter_quiz_q_score_alter_quiz_q_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='q_score',
            field=models.IntegerField(),
        ),
    ]
