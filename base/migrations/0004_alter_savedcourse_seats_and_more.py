# Generated by Django 4.2.4 on 2023-08-17 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_savedcourse_course_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedcourse',
            name='seats',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='savedcourse',
            name='seats_avail',
            field=models.IntegerField(),
        ),
    ]