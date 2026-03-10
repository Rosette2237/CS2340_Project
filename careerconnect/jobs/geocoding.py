from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable


def geocode_job(address, city, state):
    """
    Convert a job's address/city/state to (lat, lng).
    Returns (None, None) if geocoding fails or the address is not found.
    Uses OpenStreetMap Nominatim — free, no API key required.
    """
    query = f"{address}, {city}, {state}" if address else f"{city}, {state}"
    try:
        geolocator = Nominatim(user_agent="careerconnect_app")
        result = geolocator.geocode(query, timeout=5)
        if result:
            return result.latitude, result.longitude
    except (GeocoderTimedOut, GeocoderUnavailable):
        pass
    return None, None
