# Generated by Django 4.2.4 on 2024-01-01 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0003_alter_users_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('post_id', models.CharField(max_length=50)),
                ('user_message', models.CharField(default='', max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('message_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.users')),
            ],
        ),
    ]
