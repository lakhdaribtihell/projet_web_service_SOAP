import requests

def get_places(city, type_lieu):

    # 🔹 mapping type
    if type_lieu == "monument":
        tag = 'tourism=attraction'
    elif type_lieu == "restaurant":
        tag = 'amenity=restaurant'
    elif type_lieu == "parc":
        tag = 'leisure=park'
    else:
        return []

    # 🔹 1. Obtenir coordonnées avec Nominatim
    geo_url = "https://nominatim.openstreetmap.org/search"
    geo_params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    geo_response = requests.get(geo_url, params=geo_params, headers={"User-Agent": "soap-app"})
    geo_data = geo_response.json()

    if not geo_data:
        return []

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # 🔹 2. Overpass avec coordonnées
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node[{tag}](around:5000,{lat},{lon});
    );
    out;
    """

    overpass_url = "https://overpass-api.de/api/interpreter"
    response = requests.post(overpass_url, data=overpass_query)
    data = response.json()

    results = []

    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name")

        if name:
            description = f"{type_lieu} à {city}"
            results.append((description, name, type_lieu, city))

        if len(results) == 5:
            break

    return results