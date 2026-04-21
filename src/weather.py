"""
Wetterdatenabfrage für Phase 2.

Fragt historische Wetterdaten bei Visual Crossing ab.
"""

import requests
from datetime import datetime

API_KEY = "HIER_DEIN_API_KEY_EINFUEGEN"


def round_to_full_hour(dt_obj):
    """
    Rundet auf die nächste volle Stunde.
    """
    if dt_obj.minute >= 30:
        dt_obj = dt_obj.replace(minute=0, second=0, microsecond=0)
        dt_obj = dt_obj.replace(hour=dt_obj.hour)  # für Lesbarkeit
    else:
        dt_obj = dt_obj.replace(minute=0, second=0, microsecond=0)
    return dt_obj


def get_weather_for_plz(plz, dt_value):
    """
    Holt Wetterdaten für eine deutsche PLZ zu einem bestimmten Zeitpunkt.

    Parameter:
        plz: z. B. '26127'
        dt_value: datetime-Objekt oder Datumsstring

    Rückgabe:
        Temperatur in °C oder None bei Fehler
    """
    if not plz or str(plz) == "0":
        return None

    if isinstance(dt_value, str):
        dt_obj = datetime.strptime(dt_value, "%Y-%m-%d %H:%M:%S")
    else:
        dt_obj = dt_value

    dt_obj = round_to_full_hour(dt_obj)
    timestamp = dt_obj.strftime("%Y-%m-%dT%H:%M:%S")
    location = f"{plz},DE"

    url = (
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
        f"timeline/{location}/{timestamp}"
    )

    try:
        response = requests.get(
            url,
            params={
                "unitGroup": "metric",
                "key": API_KEY,
                "include": "hours"
            },
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        return data["days"][0]["temp"]

    except Exception as exc:
        print(f"Fehler bei Wetterabfrage für {plz}: {exc}")
        return None