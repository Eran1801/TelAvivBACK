# Generated by Django 4.2.4 on 2023-09-13 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0009_post_post_building_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_building_number',
            field=models.CharField(max_length=50),
        ),
    ]