import logging
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError

logger = logging.getLogger(__name__)


def geocode_job(address, city, state, country="US"):

    parts = [p for p in [address, city, state, country] if p and p.strip()]
    query = ", ".join(parts)
    if not query:
        return None, None

    try:
        geolocator = Nominatim(user_agent="careerconnect_app_gt2026")
        result = geolocator.geocode(query, timeout=10, addressdetails=False)
        if result:
            logger.info("Geocoded '%s' → (%.6f, %.6f)", query, result.latitude, result.longitude)
            return result.latitude, result.longitude
        # Retry without street address if full query returned nothing
        if address and address.strip():
            fallback = ", ".join([p for p in [city, state, country] if p and p.strip()])
            result = geolocator.geocode(fallback, timeout=10, addressdetails=False)
            if result:
                logger.info("Geocoded (fallback) '%s' → (%.6f, %.6f)", fallback, result.latitude, result.longitude)
                return result.latitude, result.longitude
        logger.warning("Geocoding returned no result for query: '%s'", query)
    except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError) as e:
        logger.error("Geocoding service error for '%s': %s", query, e)
    except Exception as e:
        logger.error("Unexpected geocoding error for '%s': %s", query, e)

    return None, None
