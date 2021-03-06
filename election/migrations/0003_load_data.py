# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-24 06:09
from __future__ import unicode_literals
import os
import csv

from django.db import migrations


def yesno(value):
    """True if yes, False if anything else"""
    return value.lower() == 'yes'


def load_states(apps, schema_editor):
    """Load states"""
    from election.choices import STATES

    State = apps.get_model('election', 'State')

    #code,state_name,is_state,senate_2018,governor_2018,automatic_vr,online_vr,
    #same_day_vr,eday_vr,early_vote_in_person,in_person_absentee,
    #early_vote_by_mail,early_vote_by_mail_fault,perm_absentee,
    #election_calendar_url,notes

    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, 'data/states.csv')

    bulk_creation = []

    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bulk_creation.append(
                State(
                    code=row['code'],
                    name=row['name'],
                    is_state=yesno(row['is_state']),
                    senate_2018=yesno(row['senate_2018']),
                    governor_2018=yesno(row['governor_2018']),
                    automatic_vr=yesno(row['automatic_vr']),
                    online_vr=yesno(row['online_vr']),
                    same_day_vr=yesno(row['same_day_vr']),
                    early_vote_in_person=yesno(row['early_vote_in_person']),
                    in_person_absentee=yesno(row['in_person_absentee']),
                    early_vote_by_mail=yesno(row['early_vote_by_mail']),
                    early_vote_by_mail_fault=yesno(
                        row['early_vote_by_mail_fault']),
                    eday_vr=yesno(row['eday_vr']),
                    has_vr=yesno(row['has_vr']),
                    perm_absentee=yesno(row['perm_absentee']),
                    early_vote_by_county=yesno(row['early_vote_by_county']),
                    election_calendar_url=row['election_calendar_url'],
                    notes=row['notes']
                ))

    State.objects.bulk_create(bulk_creation)


def destroy_states(apps, schema_editor):
    """Remove the states for reverse migrations"""
    State = apps.get_model('election', 'State')
    State.objects.all().delete()


def load_districts(apps, schema_editor):
    """Load electoral districts"""
    LegislativeDistrict = apps.get_model('election', 'LegislativeDistrict')

    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, 'data/legislative_districts.csv')

    bulk_creation = []

    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bulk_creation.append(
                LegislativeDistrict(
                    state_id=row['state'],
                    ocd_id=row['ocd_id'],
                    district_type=row['type'],
                    name=row['name']
                ))

        LegislativeDistrict.objects.bulk_create(bulk_creation)


def destroy_districts(apps, schema_editor):
    """Delete all legislative districts"""
    LegislativeDistrict = apps.get_model('election', 'LegislativeDistrict')
    LegislativeDistrict.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0002_foreign_relationships'),
    ]

    operations = [
        migrations.RunPython(load_states, destroy_states),
        migrations.RunPython(load_districts, destroy_districts)
    ]
