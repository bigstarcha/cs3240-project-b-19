from django.template.loader import get_template
from django import template

from core.models import Review

register = template.Library()


def listing_rating(listing, **options):
    _class = "starability-result"
    if "class" in options:
        _class += " " + options["class"]

    reviews = Review.objects.filter(listing=listing)
    _rating = 0

    if len(reviews) != 0:
        _rating = round(sum(review.rating for review in reviews) / len(reviews))

    _show = not (options.get("hide_if_no_reviews", False) and len(reviews) == 0)

    return {
        "class": _class,
        "rating": _rating,
        "show": _show,
    }


def review_rating(review, **options):
    _class = "starability-result"
    if "class" in options:
        _class += " " + options["class"]

    _rating = int(review.rating)

    _show = not (options.get("hide_if_no_reviews", False))

    return {
        "class": _class,
        "rating": _rating,
        "show": _show,
    }


stars_template = get_template("core/stars.html")
register.inclusion_tag(stars_template)(listing_rating)
register.inclusion_tag(stars_template)(review_rating)
