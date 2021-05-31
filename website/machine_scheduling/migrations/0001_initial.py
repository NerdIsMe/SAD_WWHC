# Generated by Django 3.1.4 on 2021-05-31 04:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='documents/raw_data')),
                ('schedule_is_done', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='StrongMachineInfo',
            fields=[
                ('index', models.IntegerField(primary_key=True, serialize=False)),
                ('startTime', models.TimeField(default=datetime.time(8, 0))),
            ],
        ),
        migrations.CreateModel(
            name='WeakMachineInfo',
            fields=[
                ('index', models.IntegerField(primary_key=True, serialize=False)),
                ('startTime', models.TimeField(default=datetime.time(8, 0))),
            ],
        ),
    ]