from hashlib import md5
from cloudinary.uploader import upload_image
import requests
from urllib.parse import urlencode
from django.core.management.base import BaseCommand

from core.models import Listing

ROOT_API_URL = "https://offgroundshousing.student.virginia.edu/bff/listing/search"
# Not really sure what this is for, just copied from a request
SEED = "1381"

headers = {
    # Seems like their server has started blocking requests from the default Requests user agent,
    # just using a less suspicious one instead :)
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}

# Listings can contain many types items in their "media collections"
# (for example, images and YouTube videos)
# This just returns the first item which is a photo (type == 2)
def get_listing_image_url(listing):
    for item in listing["mediaCollection"]:
        if item["type"] == 2:
            # Kinda hacky - for some reason some URLs include "{options}" which results in them not loading
            # No idea what we're supposed to fill in for those - just skipping for now
            if "{options}" in item["source"]:
                continue

            # Also hacky - their URLs start with "//img.offcampusimages.com"
            return "https:" + item["source"]

    return None


class Command(BaseCommand):
    help = "Scrapes offgroundshousing.student.virginia.edu for listings and saves as Listing models"

    def handle(self, *args, **options):
        metadata = requests.get(
            f"{ROOT_API_URL}/metadata?url=housing", headers=headers
        ).json()["data"]

        num_pages = metadata["totalPages"]
        num_listings = metadata["totalResults"]
        print(f"{num_pages} pages, {num_listings} listings available")

        listings = []
        for i in range(num_pages):
            params = urlencode({"url": f"housing/page-{i + 1}", "seed": SEED})
            page_listings = requests.get(
                f"https://offgroundshousing.student.virginia.edu/bff/listing/search/list?{params}",
                headers=headers,
            ).json()["data"]

            for page_listing in page_listings:
                listings.append(page_listing)

        print(f"{len(listings)} listings scraped")

        successful_listings = 0

        for listing in listings:
            image_url = get_listing_image_url(listing)

            # Since our Listing model requires an image, just ignore the listing
            if image_url is None:
                continue

            # Hashing so that multiple executions write to the same Cloudinary path
            hash = md5(image_url.encode("utf-8")).hexdigest()

            image = upload_image(image_url, public_id=hash, overwrite=False)

            Listing(
                name=listing["name"],
                latitude=listing["geography"]["latitude"],
                longitude=listing["geography"]["longitude"],
                address1=listing["geography"]["streetAddress"],
                city=listing["geography"]["cityName"],
                state=listing["geography"]["stateCode"],
                zipcode=int(listing["geography"]["zipCode"]),
                num_rooms=listing["floorPlanSummary"]["bedrooms"]["low"],
                num_bathrooms=listing["floorPlanSummary"]["bathrooms"]["low"],
                rent=listing["floorPlanSummary"]["price"]["low"],
                image=image,
            ).save()

            successful_listings += 1

        print(f"Successfully created {successful_listings} database entries")
