"""
Hauptprogramm Kühlkettenüberwachung (Minimalversion).
- Liest Daten aus dbo.coolchain (per SQL)  :contentReference[oaicite:7]{index=7}
- Prüft: Stimmigkeit, Übergaben ≤ 10 min, Transportdauer ≤ 48 h  :contentReference[oaicite:8]{index=8}
- Gibt pro Transport-ID ein klares Ergebnis aus.
"""

from db import load_records
import checks

# Company-ID für "Food Solution Hildesheim" (siehe Tests an deiner DB).
COMPANY_ID = 1703

TRANSPORT_IDS = [
    "72359278599178561029675",
    "15668407856331648336231",
    "73491878556297128760578",
    "99346757838434834886542",
    "46204863139457546291334",
    "77631003455214677542311",
    "34778534098134729847267",
    "64296734612883933474299",
    "84356113249506843372979",
    "23964376768701928340034",
    "55638471099438572108556",
    "84552276793340958450995",
    "96853785349211053482893",
    "68345254400506854834562",
    "67424886737245693583645",
    "85746762813849598680239",
    "56993454245564893300000",
    "95662334024905944384522",
    "13456783852887496020345",
    "76381745965049879836902",
]  # IDs wie im Aufgabenblatt. :contentReference[oaicite:9]{index=9}

def evaluate_one(tid: str):
    """Lädt Daten, führt 3 Checks aus und gibt (ok, meldung) zurück."""
    rows = load_records(COMPANY_ID, tid)  # (station_id, direction, datetime)
    if not rows:
        # Entspricht ID 17 im Aufgabenblatt: "Es gibt gar keinen Eintrag". :contentReference[oaicite:10]{index=10}
        return (False, "Keine Einträge zur Transport-ID gefunden.")

    ok1, msg1 = checks.check_stimmigkeit(rows)
    ok2, msg2 = checks.check_uebergabe(rows)
    ok3, msg3 = checks.check_transportdauer(rows)

    if ok1 and ok2 and ok3:
        return (True, "Kühlkette eingehalten (alle 3 Kriterien ok).")
    if not ok1:
        return (False, f"Stimmigkeit: {msg1}")
    if not ok2:
        return (False, f"Übergabe: {msg2}")
    return (False, f"Transportdauer: {msg3}")

def main():
    print("\n=== Kühlkettenüberwachung (Minimal) ===\n")
    for tid in TRANSPORT_IDS:
        ok, msg = evaluate_one(tid)
        status = "OK " if ok else "FAIL"
        print(f"{status}  ID {tid}: {msg}")
    print("\nFertig.\n")

if __name__ == "__main__":
    main()
