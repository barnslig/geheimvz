# Generated by Django 5.1.2 on 2024-11-14 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_user_image'),
        ("account", "0003_privacysettings"),

    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='can_see_profile',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_send_messages',
        ),
    ]