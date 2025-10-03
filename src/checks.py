"""
Drei Prüffunktionen gemäß Aufgabenblatt:
1) Stimmigkeit je Station (in/out-Reihenfolge)
2) Übergaben ohne Kühlung: out -> nächstes in ≤ 10 Minuten
3) Gesamttransportdauer ≤ 48 Stunden
"""

from datetime import timedelta
import math


def check_stimmigkeit(rows):
    """
    rows: Liste von Tupeln (station_id, direction, dt)
    Prüft pro Station die korrekte Reihenfolge: immer 'in' gefolgt von 'out'.
    'in' am Ende (Transport noch nicht abgeschlossen) ist erlaubt.
    Rückgabe: (ok: bool, meldung: str)
    """
    per_station = {}
    for station_id, direction, dt in rows:
        per_station.setdefault(station_id, []).append((direction, dt))

    for station_id, events in per_station.items():
        last = None
        for direction, _ in events:
            if direction not in ("in", "out"):
                return (False, f"Unbekannte Richtung '{direction}' bei Station {station_id}.")
            if last is None and direction != "in":
                return (False, f"Erster Eintrag bei Station {station_id} ist nicht 'in'.")
            if last == direction:
                return (False, f"Doppelte Richtung '{direction}' nacheinander bei Station {station_id}.")
            last = direction
        # Hinweis: endet eine Station mit 'in', ist das zulässig (Transport evtl. noch offen).

    return (True, "Stimmigkeit ok.")


def check_uebergabe(rows):
    """
    Prüft, dass zwischen einem 'out' und dem darauffolgenden 'in'
    höchstens 10 Minuten liegen.
    Rückgabe: (ok: bool, meldung: str)
    """
    prev_out = None
    for _station_id, direction, dt in rows:
        if direction == "out":
            prev_out = dt
        elif direction == "in" and prev_out is not None:
            delta = dt - prev_out
            if delta > timedelta(minutes=10):
                mins = math.ceil(delta.total_seconds() / 60.0)  # aufrunden für klare Anzeige
                return (False, f"Übergabe > 10 min: {mins} min.")
            prev_out = None
    return (True, "Übergaben ≤ 10 min.")


def check_transportdauer(rows):
    """
    Prüft, dass die Gesamttransportdauer ≤ 48 h ist.
    Rückgabe: (ok: bool, meldung: str)
    """
    if not rows:
        return (False, "Keine Einträge vorhanden.")
    start = rows[0][2]
    ende = rows[-1][2]
    delta = ende - start
    if delta > timedelta(hours=48):
        stunden = math.ceil(delta.total_seconds() / 3600.0)
        return (False, f"Transportdauer > 48h: ~{stunden} h.")
    return (True, "Transportdauer ≤ 48h.")
