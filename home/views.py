from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from home.models import Airport
import json
import requests
import threading
import time
from django.conf import settings


def map_view(request):
    airports = Airport.objects.all()
    return render(request, 'map.html', {'airports': airports})

@csrf_exempt
def get_airports(request):
    body = json.loads(request.body)
    icao = body["icao"]
    url = f"https://aviationweather.gov/api/data/airport?ids={icao}&format=json"
    resp = requests.get(url)
    data = resp.json()
    return JsonResponse(data, safe=False)


@csrf_exempt
def get_airports_within_bounds(request):
    body = json.loads(request.body)

    south = body["southwest"]["lat"]
    west = body["southwest"]["lng"]
    north = body["northeast"]["lat"]
    east = body["northeast"]["lng"]

    bbox = f"{south},{west},{north},{east}"

    url = f"https://aviationweather.gov/api/data/airport?bbox={bbox}&format=json"
    
    resp = requests.get(url)

    data = resp.json()

    airports_data = []

    for airport in data:
        airports_data.append({
            "name": airport.get("name"),
            "icao": airport.get("icaoId"),
            "lat": airport.get("lat"),
            "lon": airport.get("lon"),
        })

    return JsonResponse(airports_data, safe=False)



opensky_cache = None

def poll_opensky():
    global opensky_cache
    while True:
        try:
            res = requests.get(
                "https://opensky-network.org/api/states/all",
                timeout=30
            )
            opensky_cache = res.json()
        except Exception as e:
            print(f"Error fetching OpenSky data: {e}")

        time.sleep(45)

def planes(request):
    if opensky_cache is None:
        return JsonResponse({"error": "Data not available yet"}, status=503)
    return JsonResponse(opensky_cache)