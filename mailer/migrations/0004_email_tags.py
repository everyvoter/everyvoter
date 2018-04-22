# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-19 23:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import kennedy_common.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('branding', '0001_initial'),
        ('mailer', '0003_foreign_relationships_blocks'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('organization', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='branding.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(kennedy_common.utils.models.CacheMixinModel, models.Model),
        ),
        migrations.AddField(
            model_name='mailing',
            name='tags',
            field=models.ManyToManyField(to='mailer.EmailTags', blank=True),
        ),
        migrations.AddField(
            model_name='mailingtemplate',
            name='tags',
            field=models.ManyToManyField(to='mailer.EmailTags', blank=True),
        ),
    ]