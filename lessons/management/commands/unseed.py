"""
This is the unseeder for the database. This will delete all requests and
lessons, and will delete all users that are not admins or superusers
"""
from django.core.management.base import BaseCommand, CommandError

from lessons.models import BankTransfer,User, Request, Lesson

class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Runs database unseeding. """
        User.objects.filter(is_staff = False, is_superuser = False).delete()
        Request.objects.filter().delete()
        Lesson.objects.filter().delete()
        BankTransfer.objects.filter().delete()