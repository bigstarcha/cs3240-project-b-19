from django import forms
from localflavor.us.forms import USZipCodeField
from localflavor.us.us_states import STATE_CHOICES
from django.core.exceptions import ValidationError
from cloudinary.forms import CloudinaryFileField


class ListingForm(forms.Form):
    name = forms.CharField(max_length=500, label="Listing name")
    address1 = forms.CharField(max_length=300, label="Address")
    address2 = forms.CharField(
        max_length=300, label="Apartment #, suite, etc", required=False
    )
    city = forms.CharField(max_length=200)
    state = forms.ChoiceField(choices=STATE_CHOICES, initial="VA")
    zipcode = USZipCodeField()
    num_rooms = forms.IntegerField(label="Number of bedrooms", min_value=1)
    num_bathrooms = forms.IntegerField(label="Number of bathrooms", min_value=1)
    rent = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
        # max_value is somewhat redundant (based on max_digits)
        # but adds client-side field validation
        max_value=9999,
    )
    image = CloudinaryFileField()
    latitude = forms.FloatField()
    longitude = forms.FloatField()


def validate_rating(rating):
    if not rating in {"1", "2", "3", "4", "5"}:
        raise ValidationError("Please select a rating value", params={"value": rating})


class ReviewForm(forms.Form):
    review = forms.CharField(
        max_length=10000, label="Review Text", widget=forms.Textarea
    )
    rating_choices = (
        ("---", "---"),
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
    )

    rating = forms.ChoiceField(
        choices=rating_choices, label="Overall Rating", validators=[validate_rating]
    )
