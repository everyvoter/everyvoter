# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-23 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branding', '0004_organization_from_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='from_address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='default_organizations', to='mailer.SendingAddress', verbose_name=b'Sending Address'),
        ),
    ]