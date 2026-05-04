from db import load_records, get_connection
import checks

from temperature import check_temperature_data, print_temperature_report
from crypto_utils import load_decrypted_companies, print_company_report
from weather import get_weather_for_plz


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
]


def get_datetime_from_row(row):
    try:
        return row.datetime
    except AttributeError:
        return row[2]


def evaluate_one(tid):
    try:
        rows = load_records(COMPANY_ID, tid)
    except Exception as error:
        return False, f"Datenbankfehler: {error}"

    if not rows:
        return False, "Keine Einträge zur Transport-ID gefunden."

    ok1, msg1 = checks.check_stimmigkeit(rows)
    ok2, msg2 = checks.check_uebergabe(rows)
    ok3, msg3 = checks.check_transportdauer(rows)

    weather_info = ""

    if not ok2:
        try:
            datetime_value = get_datetime_from_row(rows[-1])
            plz = "30159"
            temp = get_weather_for_plz(plz, datetime_value)

            if temp is not None:
                weather_info = f" | Wetter: {temp} °C"
            else:
                weather_info = " | Wetterdaten nicht verfügbar"
        except Exception:
            weather_info = " | Wetterdaten nicht verfügbar"

    if ok1 and ok2 and ok3:
        return True, "Kühlkette eingehalten."

    errors = []

    if not ok1:
        errors.append(f"Stimmigkeit: {msg1}")
    if not ok2:
        errors.append(f"Übergabe: {msg2}{weather_info}")
    if not ok3:
        errors.append(f"Transportdauer: {msg3}")

    return False, " | ".join(errors)


def run_phase_1_checks():
    print("\n=== Prüfung Projektphase 1 ===\n")

    for tid in TRANSPORT_IDS:
        ok, msg = evaluate_one(tid)
        status = "OK  " if ok else "FAIL"
        print(f"{status} ID {tid}: {msg}")


def run_phase_2_checks():
    print("\n=== Erweiterungen Projektphase 2 ===\n")

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("\n--- Temperaturüberwachung ---")
        temp_violations = check_temperature_data(cursor)
        print_temperature_report(temp_violations)

        print("\n--- Entschlüsselte Firmendaten ---")
        companies = load_decrypted_companies(cursor)
        print_company_report(companies[:3])

    except Exception as error:
        print("\nFehler bei Phase 2:")
        print(error)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def main():
    print("\n===================================")
    print(" IoT-Kühlkettenüberwachung Phase 2")
    print("===================================")

    run_phase_1_checks()
    run_phase_2_checks()

    print("\nProgramm beendet.\n")


if __name__ == "__main__":
    main()