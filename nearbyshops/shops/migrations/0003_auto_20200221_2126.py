# Generated by Django 3.0.3 on 2020-02-22 03:18

from django.db import migrations
import json
from django.contrib.gis.geos import fromstr
from pathlib import Path

DATA_FILENAME = 'seeds/berlin.json'
def load_data(apps, schema_editor):
    Shop = apps.get_model('shops', 'Shop')
    jsonfile = Path(__file__).parents[2] / DATA_FILENAME

    with open(str(jsonfile), encoding="utf-8") as datafile:
        objects = json.load(datafile)
        for obj in objects['elements']:
            try:
                objType = obj['type']
                if objType == 'node':
                    tags = obj['tags']
                    name = tags.get('name','no-name')
                    longitude = obj.get('lon', 0)
                    latitude = obj.get('lat', 0)
                    location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                    Shop(name=name, location = location).save()
            except KeyError:
                pass

class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_auto_20200221_2105'),
    ]

    operations = [
    	migrations.RunPython(load_data)
    ]
