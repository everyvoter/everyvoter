# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-30 16:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geodataset', '0001_initial'),
        ('mailer', '0002_foreign_relationships'),
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='geodataset',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='geodataset.GeoDataset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailblocks',
            name='block',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blocks.Block'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailblocks',
            name='email',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mailer.Email'),
            preserve_default=False,
        ),
    ]
