# Generated by Django 5.1.2 on 2024-11-11 17:15

import core.helpers
import django.db.models.deletion
import imagekit.models.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=core.helpers.UploadToUuidFilename('groups/'), validators=[core.helpers.ValidateMaxFilesize(10)], verbose_name='Group picture')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('admins', models.ManyToManyField(related_name='groups_admin', to=settings.AUTH_USER_MODEL, verbose_name='Admins')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('members', models.ManyToManyField(related_name='groups_member', to=settings.AUTH_USER_MODEL, verbose_name='Members')),
                ('has_forum', models.BooleanField(default=True, verbose_name='Enable forum')),
                ('is_private', models.BooleanField(default=False, verbose_name='Is invite-only')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='ForumThread',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('topic', models.CharField(max_length=255, unique=True, verbose_name='Topic')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='groups.group', verbose_name='Group')),
            ],
            options={
                'verbose_name': 'Thread',
                'verbose_name_plural': 'Threads',
            },
        ),
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.TextField(verbose_name='Post')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='groups.forumthread', verbose_name='Thread')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='GroupInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('for_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='groups.group')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_invitations_sent', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_invitations_received', to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
            ],
            options={
                'verbose_name': 'Group invitation',
                'verbose_name_plural': 'Group invitations',
            },
        ),
    ]
