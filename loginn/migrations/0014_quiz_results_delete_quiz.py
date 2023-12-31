# Generated by Django 4.1 on 2023-03-22 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0013_quiz_attempts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz_Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q_score', models.IntegerField(default=0)),
                ('q_time', models.IntegerField(default=0)),
                ('quizz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loginn.quiz_info')),
                ('stu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loginn.user')),
            ],
        ),
        migrations.DeleteModel(
            name='quiz',
        ),
    ]
