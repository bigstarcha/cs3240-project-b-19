from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "core"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("tutorials", views.TutorialHomeView.as_view(), name="tutorials-homepage"),
    path(
        "tutorials/submit-listing",
        views.TutorialSubmitListingView.as_view(),
        name="tutorial-submit-listings",
    ),
    path(
        "tutorials/submit-review",
        views.TutorialSubmitReviewView.as_view(),
        name="tutorial-submit-reviews",
    ),
    path(
        "tutorials/search-listing",
        views.TutorialSearchListingView.as_view(),
        name="tutorial-search-listings",
    ),
    path(
        "tutorials/compare-listing",
        views.TutorialCompareListingView.as_view(),
        name="tutorial-compare-listings",
    ),
    path("listing/new/", views.submit_listing_view, name="submit-listing"),
    path("listing/<int:pk>/", views.listing_detail_view, name="listing-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
