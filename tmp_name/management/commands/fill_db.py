from django.core.management.base import BaseCommand
from json import load
from django.contrib.staticfiles import finders
import django.apps
from functools import reduce


class Command(BaseCommand):
    help = 'Command for developing and tests'

    def handle(self, *args, **options):
        stub = load(open('backend/static/stubs/db.json'))
        for class_model, full_name in map(lambda o: (o, str(o)), django.apps.apps.get_models()):
            name = full_name.split('.')[-1].replace("'>", '')
            eggs = stub.get(f'{name}Collection', [])
            class_model.objects.all().delete()
            for egg in eggs:
                model = class_model(**egg)
                model.save()
                print(f'{model} is created')
