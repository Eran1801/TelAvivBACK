# Generated by Django 4.2.4 on 2024-01-04 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inbox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinbox',
            name='read_status',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
