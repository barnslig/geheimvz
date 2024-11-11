from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.crypto import get_random_string
import re

from core.models import User
from invites.models import InviteCode


def generate_code(name: str, length: int):
    code = re.sub(r"[^A-Z]", "", name[:4].upper())
    remaining = length - len(code)
    code += get_random_string(remaining, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return code


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            with transaction.atomic():
                InviteCode.objects.filter(owner=user).delete()
                code = InviteCode()
                code.owner = user
                code.code = generate_code(user.display_name, 12)
                code.remaining = 2
                code.save()

        self.stdout.write(self.style.SUCCESS("Successfully created codes"))
