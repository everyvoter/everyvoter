# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 20:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0001_initial'),
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingblocks',
            name='mailing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mailer.Mailing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='templateblocks',
            name='template',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mailer.MailingTemplate'),
            preserve_default=False,
        ),
    ]