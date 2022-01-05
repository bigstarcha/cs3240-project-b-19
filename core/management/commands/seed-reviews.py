from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import lorem
from random import random

from core.models import Listing, Review

User = get_user_model()


class Command(BaseCommand):
    help = "Adds mock reviews to existing listings"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete all previously created reviews",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            Review.objects.all().delete()

        try:
            test_user = User.objects.get(username="__test__")
        except:
            print("Test user does not exist, creating")
            test_user = User.objects.create(
                username="__test__",
                first_name="Lorem",
            )
            test_user.save()

        # Get all listings
        listings = Listing.objects.all()

        for listing in listings:
            for _ in range(int(random() * 5)):
                Review(
                    rating=int(random() * 4) + 1,
                    review=lorem.paragraph(),
                    date=timezone.now(),
                    listing=listing,
                    user=test_user,
                ).save()
