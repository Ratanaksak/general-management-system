# Generated by Django 5.1.2 on 2025-04-26 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_person_commune_kh_name_person_district_kh_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='commune_kh_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='district_kh_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='province_kh_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='village_kh_name',
        ),
    ]
