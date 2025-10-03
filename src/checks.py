"""
Prüffunktionen gemäß Aufgabenblatt:
1) Stimmigkeit je Station (in/out-Reihenfolge)
2) Übergaben ohne Kühlung: out -> nächstes in ≤ 10 Minuten
3) Gesamttransportdauer ≤ 48 Stunden
"""
from datetime import timedelta

def check_stimmigkeit(rows):
    """
    Prüft pro Station die sinnvolle Reihenfolge 'in' -> 'out'.
    Rückgabe: (ok: bool, meldung: str)
    """
    station_events = {}
    for (company, tid, station, category, direction, dt) in rows:
        station_events.setdefault(station, []).append((direction, dt))

    for station, events in station_events.items():
        last_dir = None
        for direction, _dt in events:
            if direction not in ("in", "out"):
                return (False, f"Unbekannte Richtung '{direction}' bei {station}.")
            if last_dir is None and direction != "in":
                return (False, f"Erster Eintrag bei {station} ist nicht 'in'.")
            if last_dir == direction:
                return (False, f"Doppelte Richtung '{direction}' nacheinander bei {station}.")
            last_dir = direction
        # Hinweis: wenn der letzte Eintrag 'in' ist (Transport noch nicht ausgecheckt),
        # ist das laut Aufgabenblatt kein Fehler.

    return (True, "Stimmigkeit ok.")

def check_uebergabe(rows):
    """
    Prüft, dass zwischen 'out' und nächstem 'in' höchstens 10 Minuten liegen.
    Rückgabe: (ok: bool, meldung: str)
    """
    prev_out_time = None
    for (_c, _tid, _station, _cat, direction, dt) in rows:
        if direction == "out":
            prev_out_time = dt
        elif direction == "in" and prev_out_time is not None:
            delta = dt - prev_out_time
            if delta > timedelta(minutes=10):
                return (False, f"Übergabe > 10 min: {int(delta.total_seconds() // 60)} min.")
            prev_out_time = None
    return (True, "Übergaben ≤ 10 min.")

def check_transportdauer(rows):
    """
    Prüft, dass die gesamte Transportdauer ≤ 48 Stunden ist.
    Rückgabe: (ok: bool, meldung: str)
    """
    if not rows:
        return (False, "Keine Einträge vorhanden.")
    start = rows[0][-1]   # erstes datetime
    ende  = rows[-1][-1]  # letztes datetime
    delta = ende - start
    if delta > timedelta(hours=48):
        return (False, f"Transportdauer > 48h: ~{int(delta.total_seconds() // 3600)} h.")
    return (True, "Transportdauer ≤ 48h.")
