# Generated by Django 4.1 on 2023-03-22 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginn', '0014_quiz_results_delete_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coins',
            field=models.IntegerField(default=0, max_length=100),
        ),
    ]