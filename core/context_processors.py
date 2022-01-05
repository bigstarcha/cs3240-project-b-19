from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Makes the Google Maps API key accessbile in all templates
def api_key(request):
    return {"GOOGLE_API_KEY": getenv("GOOGLE_API_KEY")}
