# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Online',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'online',
            },
        ),
    ]
