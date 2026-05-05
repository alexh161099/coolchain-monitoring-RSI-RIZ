"""
@file weather.py
@brief Wetterdatenabfrage für Projektphase 2.

Fragt historische Wetterdaten über die Visual-Crossing-API ab.
"""

import time
import requests
from datetime import datetime


API_KEY = "R8L9F6Y28G4QVPA2VP7ECQCE6"

# Zwischenspeicher, damit gleiche Wetterabfragen nicht mehrfach an die API gehen
weather_cache = {}


def round_to_full_hour(dt_obj):
    """
    @brief Rundet einen Zeitpunkt auf die volle Stunde ab.

    @param dt_obj Zeitpunkt als datetime-Objekt.
    @return Gerundeter Zeitpunkt.
    """
    return dt_obj.replace(minute=0, second=0, microsecond=0)


def get_weather_for_plz(plz, dt_value):
    """
    @brief Holt Wetterdaten für eine deutsche PLZ zu einem bestimmten Zeitpunkt.

    @param plz Postleitzahl, z. B. "26127".
    @param dt_value datetime-Objekt oder String im Format YYYY-MM-DD HH:MM:SS.
    @return Temperatur in °C oder None bei Fehler.
    """
    if not plz or str(plz) == "0":
        return None

    if API_KEY == "DEIN_API_KEY_HIER_EINFUEGEN" or not API_KEY:
        return None

    try:
        if isinstance(dt_value, str):
            dt_obj = datetime.strptime(dt_value, "%Y-%m-%d %H:%M:%S")
        else:
            dt_obj = dt_value

        dt_obj = round_to_full_hour(dt_obj)

        cache_key = f"{plz}_{dt_obj.strftime('%Y-%m-%dT%H:%M:%S')}"

        if cache_key in weather_cache:
            return weather_cache[cache_key]

        timestamp = dt_obj.strftime("%Y-%m-%dT%H:%M:%S")
        location = f"{plz},DE"

        url = (
            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
            f"timeline/{location}/{timestamp}"
        )

        # kleine Pause gegen zu viele direkte Anfragen
        time.sleep(1)

        response = requests.get(
            url,
            params={
                "unitGroup": "metric",
                "key": API_KEY,
                "include": "hours",
            },
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        temp = data["days"][0]["temp"]

        weather_cache[cache_key] = temp

        return temp

    except requests.exceptions.HTTPError as error:
        if error.response is not None and error.response.status_code == 429:
            print("Wetter-API Limit erreicht. Bitte später erneut versuchen.")
        else:
            print(f"Wetterdaten konnten für PLZ {plz} nicht geladen werden.")
        return None

    except Exception:
        print(f"Wetterdaten konnten für PLZ {plz} nicht geladen werden.")
        return None