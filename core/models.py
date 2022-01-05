# References used: https://docs.djangoproject.com/en/3.2/ref/models/fields/#decimalfield
#                  https://cloudinary.com/documentation/django_integration

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Listing(models.Model):

    name = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    # client-side picker: how to implement this?
    zipcode = models.PositiveIntegerField()
    num_rooms = models.PositiveIntegerField()
    num_bathrooms = models.PositiveIntegerField()
    rent = models.DecimalField(max_digits=6, decimal_places=2)
    image = CloudinaryField("image")

    def __str__(self):
        return f"{self.name} ({self.num_rooms}x{self.num_bathrooms}, ${self.rent})"


class Review(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.CharField(max_length=10000)
    date = models.DateTimeField("Date Published")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (
            str(self.rating)
            + ", "
            + str(self.date)
            + ", "
            + str(self.listing)
            + ", "
            + str(self.user)
        )
