import httpx
from dotenv import load_dotenv
import os
from models import Destination

load_dotenv()

class SkyscannerAPI:
    async def get_flights(self, origin: str, destination: str, date: str):
        url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/APIs/flights"
        headers = {
            "X-RapidAPI-Key": os.getenv("SKYSCANNER_API_KEY"),
            "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }
        params = {"origin": origin, "destination": destination, "date": date}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return {"price": data.get("quotes", [{}])[0].get("price", 0)}

class GoogleMapsAPI:
    async def get_route(self, origin: str, destination: str):
        url = f"https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "key": os.getenv("GOOGLE_MAPS_API_KEY")
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            distance = data["routes"][0]["legs"][0]["distance"]["value"] / 1000  # km
            duration = data["routes"][0]["legs"][0]["duration"]["value"] / 3600  # hours
            return {"distance_km": distance, "duration_hours": duration}

class TripAdvisorAPI:
    async def get_activities(self, location: str, interests: list):
        url = "https://api.tripadvisor.com/api/activities"
        headers = {"Authorization": f"Bearer {os.getenv('TRIPADVISOR_API_KEY')}"}
        params = {"location": location, "categories": ",".join(interests)}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return [{"name": item["name"], "cost": item.get("price", 50)} for item in data.get("activities", [])]
