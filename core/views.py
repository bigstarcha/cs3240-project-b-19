"""
Complete list of all citations including authors, versions, dates, and urls: https://github.com/uva-cs3240-f21/project-b-19/blob/main/citations.md
In this file:
- Google Login Tutorial (https://www.section.io/engineering-education/django-google-oauth/)
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse
from datetime import datetime
from django.utils.timezone import make_aware
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
import json

from datetime import date

from core.forms import ListingForm, ReviewForm
from .models import Listing, Review


def index_view(request):
    search_string = request.GET.get("search") or ""
    listings = Listing.objects.filter(
        Q(name__icontains=search_string)
        | Q(address1__icontains=search_string)
        | Q(address2__icontains=search_string)
        | Q(city__icontains=search_string)
        | Q(state__icontains=search_string)
        | Q(zipcode__icontains=search_string)
    )
    listings_serialized = serializers.serialize("json", listings)
    return render(
        request,
        "core/index.html",
        {"listings": listings, "listings_serialized": listings_serialized},
    )


class TutorialHomeView(generic.TemplateView):
    template_name = "core/tutorial-homepage.html"


class TutorialSubmitListingView(generic.TemplateView):
    template_name = "core/tutorial-submit-listings.html"


class TutorialSubmitReviewView(generic.TemplateView):
    template_name = "core/tutorial-submit-reviews.html"


class TutorialSearchListingView(generic.TemplateView):
    template_name = "core/tutorial-search-listings.html"


class TutorialCompareListingView(generic.TemplateView):
    template_name = "core/tutorial-compare-listings.html"


@login_required
def submit_listing_view(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = Listing(
                name=form.cleaned_data["name"],
                latitude=form.cleaned_data["latitude"],
                longitude=form.cleaned_data["longitude"],
                address1=form.cleaned_data["address1"],
                address2=form.cleaned_data["address2"],
                city=form.cleaned_data["city"],
                state=form.cleaned_data["state"],
                zipcode=form.cleaned_data["zipcode"],
                num_rooms=form.cleaned_data["num_rooms"],
                num_bathrooms=form.cleaned_data["num_bathrooms"],
                rent=form.cleaned_data["rent"],
                image=form.cleaned_data["image"],
            )

            new_listing.save()

            return HttpResponseRedirect(
                reverse("core:listing-detail", args=(new_listing.id,))
            )

    else:
        form = ListingForm()

    return render(request, "core/submit-listing.html", {"form": form})


def listing_detail_view(request, pk):
    listing = get_object_or_404(Listing.objects.all(), id=pk)
    reviews = Review.objects.filter(listing=listing)
    average = 0.0
    if len(reviews) > 0:
        average = round(sum([review.rating for review in reviews]) / len(reviews), 2)

    form = ReviewForm()

    previous_review = None

    if request.user.is_authenticated:
        try:
            previous_review = Review.objects.get(user=request.user, listing=listing)
        except Review.DoesNotExist:
            pass

        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                date = make_aware(datetime.now())
                review, review_created = Review.objects.update_or_create(
                    listing=listing,
                    user=request.user,
                    defaults={
                        "review": form.cleaned_data["review"],
                        "rating": form.cleaned_data["rating"],
                        "date": date,
                    },
                )

                review.save()

                return HttpResponseRedirect(
                    reverse("core:listing-detail", args=(listing.id,))
                )

    return render(
        request,
        "core/listing-detail.html",
        {
            "form": form,
            "listing": listing,
            "average": average,
            "reviews": reviews,
            "previous_review_id": previous_review.id if previous_review else None,
            "previous_review": json.dumps(
                model_to_dict(previous_review), cls=DjangoJSONEncoder
            )
            if previous_review
            else None,
        },
    )
