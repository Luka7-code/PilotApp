import csv
from home.models import Airport


def import_airports():
    with open('L:\\Projects\\PilotApp\\airports.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        airports_to_add = []

        for row in reader:
            airport = Airport(
                icao_code=row['ident'],
                name=row['name'],
                latitude=float(row['latitude_deg']),
                longitude=float(row['longitude_deg']),
                type=row['type']
            )
            airports_to_add.append(airport)

            # Commit in batches of 100 to improve performance (adjust as needed)
            if len(airports_to_add) >= 100:
                Airport.objects.bulk_create(airports_to_add)
                airports_to_add.clear()  # Reset the list after bulk insertion

        # Insert any remaining airports (less than 100)
        if airports_to_add:
            Airport.objects.bulk_create(airports_to_add)