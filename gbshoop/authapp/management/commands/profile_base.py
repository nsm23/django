import json

from django.core.management.base import BaseCommand

from authapp.models import Gbuser, GbUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in Gbuser.objects.filter(gbuserprofile__isnull=True):
            GbUserProfile.objects.create(user=user)
