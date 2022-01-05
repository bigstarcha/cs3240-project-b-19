from http import HTTPStatus
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.urls import reverse
from cloudinary import CloudinaryImage, CloudinaryResource
from http import HTTPStatus
from unittest.mock import patch

from django.test import TestCase

from .models import Listing, Review


class SubmitListingViewTests(TestCase):
    # Creating mock images to pass in form POST bodies
    @staticmethod
    def get_image_file():
        return SimpleUploadedFile(
            "file.png", b"fake image data", content_type="image/png"
        )

    def post_with_cloudinary_mock(self, url, data):
        with patch(
            "cloudinary.uploader.upload_image", return_value=CloudinaryImage()
        ) as mock_upload:
            response = self.client.post(url, data=data)

        self.assertTrue(mock_upload.called)

        return response

    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username="testuser")
        user.set_password("MyPassword")
        user.save()

    def test_entrypoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Submit a listing", html=True)

    def test_login_required(self):
        response = self.client.get("/listing/new/")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            response["Location"], "/accounts/google/login/?next=/listing/new/"
        )

        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        response = self.client.get("/listing/new/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_success(self):
        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        response = self.post_with_cloudinary_mock(
            "/listing/new/",
            data={
                "name": "105 Valley Road",
                "address1": "105 Valley Road",
                "address2": "Unit A",
                "city": "Charlottesville",
                "state": "VA",
                "zipcode": 22903,
                "num_rooms": 3,
                "num_bathrooms": 2,
                "rent": 1850,
                "latitude": 38.0304917,
                "longitude": -78.5076235,
                "image": self.get_image_file(),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/listing/1/")

        response = self.client.get("/")
        self.assertContains(response, "105 Valley Road", html=True)

    def test_post_address2_optional(self):
        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        response = self.post_with_cloudinary_mock(
            "/listing/new/",
            data={
                "name": "105 Valley Road",
                "address1": "105 Valley Road",
                "city": "Charlottesville",
                "state": "VA",
                "zipcode": 22903,
                "num_rooms": 3,
                "num_bathrooms": 2,
                "rent": 1850,
                "latitude": 38.0304917,
                "longitude": -78.5076235,
                "image": self.get_image_file(),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/listing/1/")

        response = self.client.get("/")
        self.assertContains(response, "105 Valley Road", html=True)

    def test_post_failure_zipcode(self):
        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        response = self.post_with_cloudinary_mock(
            "/listing/new/",
            data={
                "name": "105 Valley Road",
                "address1": "105 Valley Road",
                "address2": "Unit A",
                "city": "Charlottesville",
                "state": "VA",
                "zipcode": 0,  # not a valid zipcode
                "num_rooms": 3,
                "num_bathrooms": 2,
                "rent": 1850,
                "latitude": 38.0304917,
                "longitude": -78.5076235,
                "image": self.get_image_file(),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "Enter a zip code in the format XXXXX or XXXXX-XXXX.", html=True
        )

    def test_post_failure_negative_values(self):
        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        response = self.post_with_cloudinary_mock(
            "/listing/new/",
            data={
                "name": "105 Valley Road",
                "address1": "105 Valley Road",
                "address2": "Unit A",
                "city": "Charlottesville",
                "state": "VA",
                "zipcode": 22903,
                "num_rooms": -3,
                "num_bathrooms": -2,
                "rent": -1850,
                "latitude": 38.0304917,
                "longitude": -78.5076235,
                "image": self.get_image_file(),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
            "Ensure this value is greater than or equal to 1.",
            count=2,
            html=True,
        )
        self.assertContains(
            response,
            "Ensure this value is greater than or equal to 0.",
            count=1,
            html=True,
        )

    def test_post_failure_max_rent(self):
        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        response = self.post_with_cloudinary_mock(
            "/listing/new/",
            data={
                "name": "105 Valley Road",
                "address1": "105 Valley Road",
                "address2": "Unit A",
                "city": "Charlottesville",
                "state": "VA",
                "zipcode": 22903,
                "num_rooms": 3,
                "num_bathrooms": 2,
                "rent": 10000,
                "latitude": 38.0304917,
                "longitude": -78.5076235,
                "image": self.get_image_file(),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
            "Ensure that there are no more than 4 digits before the decimal point.",
            html=True,
        )


class ReviewDetailViewTests(TestCase):
    # Creating mock images to pass in form POST bodies
    @staticmethod
    def get_image_file():
        return SimpleUploadedFile(
            "file.png", b"fake image data", content_type="image/png"
        )

    def create_test_listing(
        self,
        name="Test Listing",
        latitude=38.03640,
        longitude=-78.50732,
        address1="400 Emmet St S",
        city="Charlottesville",
        state="Virginia",
        zipcode="22903",
        num_rooms=4,
        num_bathrooms=2,
        rent=2000,
    ):
        with patch(
            "cloudinary.uploader.upload_resource", return_value=CloudinaryResource()
        ) as mock_upload:
            listing = Listing.objects.create(
                name=name,
                latitude=latitude,
                longitude=longitude,
                address1=address1,
                city=city,
                state=state,
                zipcode=zipcode,
                num_rooms=num_rooms,
                num_bathrooms=num_bathrooms,
                rent=rent,
                image=self.get_image_file(),
            )

            self.assertTrue(mock_upload.called)
        return listing

    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username="testuser")
        user.set_password("MyPassword")
        user.save()

    def test_entrypoint(self):
        listing = self.create_test_listing()

        url = reverse("core:listing-detail", args=(listing.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Test Listing", html=True)

    def test_post_success(self):
        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        listing = self.create_test_listing()

        self.assertFalse(Review.objects.filter(id=1))

        time = timezone.now()
        response = self.client.post(
            reverse("core:listing-detail", args=(listing.id,)),
            data={
                "rating": 3,
                "review": "Neutral review",
                "date": time,
                "listing": listing,
                "user": get_user_model().objects.get(username="testuser"),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            response["Location"], reverse("core:listing-detail", args=(listing.id,))
        )
        self.assertTrue(Review.objects.filter(id=1))

    def test_update_review(self):
        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        listing = self.create_test_listing()

        time = timezone.now()
        self.client.post(
            reverse("core:listing-detail", args=(listing.id,)),
            data={
                "rating": 3,
                "review": "Neutral review",
                "date": time,
                "listing": listing,
                "user": get_user_model().objects.get(username="testuser"),
            },
        )

        review = Review.objects.filter(id=1)[0]

        self.assertEqual(review.rating, 3)
        self.assertEqual(review.review, "Neutral review")

        self.client.post(
            reverse("core:listing-detail", args=(listing.id,)),
            data={
                "rating": 5,
                "review": "Positive review",
                "date": time,
                "listing": listing,
                "user": get_user_model().objects.get(username="testuser"),
            },
        )
        review = Review.objects.filter(id=1)[0]

        self.assertEqual(review.rating, 5)
        self.assertEqual(review.review, "Positive review")

    def test_post_failure_no_rating_selected(self):
        logged_in = self.client.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

        listing = self.create_test_listing()

        time = timezone.now()
        response = self.client.post(
            reverse("core:listing-detail", args=(listing.id,)),
            data={
                "rating": "---",
                "review": "Neutral review",
                "date": time,
                "listing": listing,
                "user": get_user_model().objects.get(username="testuser"),
            },
        )

        # Status code would be a 302 Found if form had been submitted correctly
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Confirm that entry was not created in the database
        self.assertFalse(Review.objects.filter(id=1))
