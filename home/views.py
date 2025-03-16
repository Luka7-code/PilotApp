from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from home.models import Airport
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