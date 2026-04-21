"""
Temperaturüberwachung für Phase 2.

Prüft Temperaturdaten aus der Tabelle tempdata.
Laut Aufgabenstellung müssen die Temperaturen zwischen +2 °C und +4 °C liegen.
"""

def check_temperature_data(cursor):
    """
    Liest alle Temperaturdaten aus tempdata und gibt Verstöße zurück.

    Rückgabe:
        Liste mit Dictionaries:
        [
            {
                "station_id": 12,
                "datetime": datetime_obj,
                "temperature": 5.2,
                "message": "Temperatur außerhalb des erlaubten Bereichs"
            }
        ]
    """
    query = """
        SELECT transportstationID, [datetime], temperature
        FROM dbo.tempdata
        ORDER BY [datetime] ASC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    violations = []

    for row in rows:
        station_id = row[0]
        dt = row[1]
        temp = row[2]

        if temp < 2 or temp > 4:
            violations.append({
                "station_id": station_id,
                "datetime": dt,
                "temperature": temp,
                "message": "Temperatur außerhalb des erlaubten Bereichs"
            })

    return violations


def print_temperature_report(violations):
    """
    Gibt einen einfachen Bericht zu Temperaturverstößen aus.
    """
    print("\n=== Temperaturüberwachung ===")

    if not violations:
        print("OK: Keine Temperaturverstöße gefunden.")
        return

    print(f"FAIL: {len(violations)} Temperaturverstöße gefunden:")
    for v in violations:
        print(
            f"Station {v['station_id']} | "
            f"Zeit: {v['datetime']} | "
            f"Temperatur: {v['temperature']} °C | "
            f"{v['message']}"
        )