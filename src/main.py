"""
Hauptprogramm Kühlkettenüberwachung (Minimalversion).

- Liest Daten aus dbo.coolchain für die vorgegebenen 20 Transport-IDs
- Prüft Stimmigkeit, Übergaben und Transportdauer
- Gibt pro ID ein klares Ergebnis mit evtl. Fehlerbeschreibung aus
"""
from db import load_records
from checks import check_stimmigkeit, check_uebergabe, check_transportdauer

COMPANY = "Food Solution Hildesheim"

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
]

def evaluate_one(tid: str):
    """Lädt Daten, führt 3 Checks aus und gibt (ok, meldung) zurück."""
    rows = load_records(COMPANY, tid)
    if not rows:
        return (False, "Keine Einträge zur Transport-ID gefunden.")

    ok1, msg1 = check_stimmigkeit(rows)
    ok2, msg2 = check_uebergabe(rows)
    ok3, msg3 = check_transportdauer(rows)

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
