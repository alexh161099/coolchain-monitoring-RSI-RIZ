"""
Temperaturüberwachung für Projektphase 2.
Prüft, ob die Temperaturen der Kühlstationen im Bereich +2 °C bis +4 °C liegen.
"""


def check_temperature_data(cursor):
    """
    Liest Temperaturdaten aus dbo.tempdata und gibt alle Grenzwertverstöße zurück.
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
        temperature = row[2]

        if temperature < 2 or temperature > 4:
            violations.append(
                {
                    "station_id": station_id,
                    "datetime": dt,
                    "temperature": temperature,
                    "message": "Temperatur außerhalb des erlaubten Bereichs",
                }
            )

    return violations


def print_temperature_report(violations):
    """
    Gibt die gefundenen Temperaturverstöße übersichtlich aus.
    """
    print("\n=== Temperaturüberwachung ===")

    if not violations:
        print("OK: Keine Temperaturverstöße gefunden.")
        return

    print(f"FAIL: {len(violations)} Temperaturverstöße gefunden:")

    for violation in violations:
        print(
            f"Station {violation['station_id']} | "
            f"Zeit: {violation['datetime']} | "
            f"Temperatur: {violation['temperature']} °C | "
            f"{violation['message']}"
        )