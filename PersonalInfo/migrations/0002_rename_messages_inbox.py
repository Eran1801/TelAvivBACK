# Generated by Django 4.2.4 on 2023-12-24 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalInfo', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messages',
            new_name='Inbox',
        ),
    ]