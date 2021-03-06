# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-09 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0005_template_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailactivity',
            name='mailing',
        ),
        migrations.RemoveField(
            model_name='unsubscribe',
            name='mailing',
        ),
        migrations.AddField(
            model_name='emailactivity',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailer.Email'),
        ),
        migrations.AddField(
            model_name='unsubscribe',
            name='address',
            field=models.EmailField(default='help@localhost', max_length=254, verbose_name=b'Email Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='unsubscribe',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailer.Email'),
        ),
    ]
