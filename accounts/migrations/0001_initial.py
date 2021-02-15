# Generated by Django 3.1.6 on 2021-02-12 20:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('login', models.CharField(max_length=200, unique=True, verbose_name='login')),
                ('password', models.CharField(max_length=200, verbose_name='password')),
                ('is_archive', models.BooleanField(default=True)),
                ('role', models.CharField(max_length=255, verbose_name='Role')),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]
