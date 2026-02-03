from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from home.models import Airport
import requests
from django.conf import settings
from django.http import JsonResponse
from django.core.cache import cache
from .utils import fetch_metar
import json


def map_view(request):
    airports = Airport.objects.all()
    return render(request, 'map.html', {'airports': airports})


@csrf_exempt
def get_airports_within_bounds(request):
    # Parse the request body to get the bounds and zoom level
    data = json.loads(request.body)
    southwest = data['southwest']
    northeast = data['northeast']
    zoom_level = data['zoom_level']

    # Filter airports based on the bounds
    airports = Airport.objects.filter(
        latitude__gte=southwest['lat'],
        latitude__lte=northeast['lat'],
        longitude__gte=southwest['lng'],
        longitude__lte=northeast['lng']
    )

    if zoom_level <=4:
        airports = airports.filter(type='large_airport')
    else:
        pass

    # Prepare the airports to return as JSON
    airports_data = [{'name': airport.name, 'latitude': airport.latitude, 'longitude': airport.longitude, 'icao_code': airport.icao_code} for airport in airports]

    return JsonResponse(airports_data, safe=False)

def fetch_metar(icao):
    url = f"https://api.checkwx.com/metar/{icao}/decoded"
    headers = {
        "X-API-Key": settings.CHECKWX_API_KEY
    }
    r = requests.get(url, headers=headers, timeout=10)

    if r.status_code != 200:
        return None

    data = r.json()
    if not data.get("data"):
        return None

    return data["data"][0]

def weather_bulk(request):
    icaos = request.GET.getlist("icao[]")
    results = {}

    for icao in icaos:
        cache_key = f"metar_{icao}"
        metar = cache.get(cache_key)

        if not metar:
            metar = fetch_metar(icao)
            if metar:
                cache.set(cache_key, metar, 600)  # 10 min

        if metar:
            results[icao] = metar

    return JsonResponse(results)