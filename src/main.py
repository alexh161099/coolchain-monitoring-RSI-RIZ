"""
@file main.py
@brief Hauptprogramm der IoT-Kühlkettenüberwachung.

Dieses Programm stellt eine Konsolenoberfläche bereit und verbindet die Prüfungen
aus Projektphase 1 mit den Erweiterungen aus Projektphase 2.

@details
- Projektphase 1: Stimmigkeit, Übergabe, Transportdauer prüfen
- Projektphase 2: Temperaturüberwachung, entschlüsselte Firmendaten, Wetterdaten

@date 05.2026
@author Fynn Bremer, Alexander Holzenkamp, Tom Stoelken
"""

from db import load_records, get_connection, load_station_plz
import checks
from temperature import check_temperature_data, print_temperature_report
from crypto_utils import load_decrypted_companies, print_company_report
from weather import get_weather_for_plz

import contextlib
import io
import threading
import traceback
import tkinter as tk
from tkinter import ttk, scrolledtext


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
    """
    @brief Ermittelt den Zeitstempel aus einem Datenbankdatensatz.

    @param row Datensatz aus der Datenbank.
    @return Zeitstempel des Datensatzes.
    """
    try:
        return row.datetime
    except AttributeError:
        return row[2]


def get_station_id_from_row(row):
    """
    @brief Ermittelt die Transportstations-ID aus einem Datenbankdatensatz.

    @param row Datensatz aus der Datenbank.
    @return Transportstations-ID.
    """
    try:
        return row.station_id
    except AttributeError:
        return row[0]


def evaluate_one(tid):
    """
    @brief Prüft eine einzelne Transport-ID.

    Die Funktion prüft Stimmigkeit, Übergabezeit und Transportdauer.
    Bei Übergabefehlern wird zusätzlich die Wettertemperatur am Übergabeort abgefragt.

    @param tid Transport-ID als Zeichenkette.
    @return Tupel aus Statuswert und Meldung.
    """
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
            station_id = get_station_id_from_row(rows[-1])

            # PLZ wird zuerst dynamisch über die Transportstation geladen.
            plz = load_station_plz(station_id)

            # Falls z. B. ein Kühltransporter keine PLZ besitzt, wird eine Fallback-PLZ verwendet.
            if not plz or str(plz) == "0":
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
    """
    @brief Führt die Prüfungen aus Projektphase 1 aus.
    """
    print("\n=== Prüfung Projektphase 1 ===\n")

    for tid in TRANSPORT_IDS:
        ok, msg = evaluate_one(tid)
        status = "OK  " if ok else "FAIL"
        print(f"{status} ID {tid}: {msg}")


def run_phase_2_checks():
    """
    @brief Führt die Erweiterungen aus Projektphase 2 aus.
    """
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


def show_menu():
    """
    @brief Stellt die Konsolenbedienung bereit.

    Der Benutzer kann auswählen, ob Projektphase 1, Projektphase 2
    oder beide Prüfungen ausgeführt werden sollen.
    """
    while True:
        print("\n===================================")
        print(" IoT-Kühlkettenüberwachung Phase 2")
        print("===================================")
        print("1 - Projektphase 1 prüfen")
        print("2 - Projektphase 2 Erweiterungen prüfen")
        print("3 - Alles ausführen")
        print("0 - Programm beenden")

        choice = input("\nAuswahl eingeben: ")

        if choice == "1":
            run_phase_1_checks()
        elif choice == "2":
            run_phase_2_checks()
        elif choice == "3":
            run_phase_1_checks()
            run_phase_2_checks()
        elif choice == "0":
            print("\nProgramm beendet.\n")
            break
        else:
            print("\nUngültige Eingabe. Bitte erneut versuchen.")


def capture_output(func, *args, **kwargs):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue()


def run_phase_1_checks_text(tid_list=None):
    if tid_list is None:
        tid_list = TRANSPORT_IDS

    lines = ["=== Prüfung Projektphase 1 ==="]
    for tid in tid_list:
        ok, msg = evaluate_one(tid)
        status = "OK" if ok else "FAIL"
        lines.append(f"{status} | ID {tid} | {msg}")

    return "\n".join(lines)


def run_phase_2_checks_text():
    return capture_output(run_phase_2_checks)


class CoolchainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kühlketten-Monitoring Übersicht")
        self.geometry("900x650")
        self.minsize(860, 620)
        self.configure(bg="#f2f5fb")

        style = ttk.Style(self)
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="#f2f5fb")
        style.configure("TLabel", background="#f2f5fb")
        style.configure("TButton", padding=6)

        self._task_thread = None
        self._task_result = ""
        self._task_error = None

        self._build_header()
        self._build_controls()
        self._build_output_area()
        self._build_status_bar()

    def _build_header(self):
        header_frame = ttk.Frame(self, padding=(20, 12, 20, 6))
        header_frame.pack(fill="x")

        title = ttk.Label(
            header_frame,
            text="IoT-Kühlkettenüberwachung",
            style="Header.TLabel",
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header_frame,
            text=(
                "Projektphase 1: Stimmigkeit, Übergabe, Transportdauer prüfen. "
                "Projektphase 2: Temperaturüberwachung und entschlüsselte Firmendaten."
            ),
            wraplength=820,
            justify="left",
        )
        subtitle.pack(anchor="w", pady=(6, 0))

    def _build_controls(self):
        controls_frame = ttk.Frame(self, padding=(20, 10, 20, 10))
        controls_frame.pack(fill="x")

        id_label = ttk.Label(controls_frame, text="Transport-ID (optional):")
        id_label.grid(row=0, column=0, sticky="w")

        self.transport_id_entry = ttk.Entry(controls_frame, width=42)
        self.transport_id_entry.grid(row=0, column=1, sticky="w", padx=(10, 0))

        ttk.Button(
            controls_frame,
            text="Phase 1 prüfen",
            command=self.on_run_phase_1,
        ).grid(row=0, column=2, padx=10, pady=4)

        ttk.Button(
            controls_frame,
            text="Phase 2 prüfen",
            command=self.on_run_phase_2,
        ).grid(row=0, column=3, padx=10, pady=4)

        ttk.Button(
            controls_frame,
            text="Alle prüfen",
            command=self.on_run_all,
        ).grid(row=0, column=4, padx=10, pady=4)

        ttk.Button(
            controls_frame,
            text="Nur diese ID prüfen",
            command=self.on_run_single_id,
        ).grid(row=0, column=5, padx=10, pady=4)

        info_label = ttk.Label(
            controls_frame,
            text=f"Firma ID: {COMPANY_ID} | Anzahl Standard-Transport-IDs: {len(TRANSPORT_IDS)}",
            foreground="#444444",
        )
        info_label.grid(row=1, column=0, columnspan=6, sticky="w", pady=(10, 0))

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=(0, 10))

    def _build_output_area(self):
        output_frame = ttk.Frame(self, padding=(20, 0, 20, 0))
        output_frame.pack(fill="both", expand=True)

        label = ttk.Label(output_frame, text="Ausgabeübersicht:")
        label.pack(anchor="w", pady=(0, 6))

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap="word",
            height=24,
            font=("Consolas", 10),
            background="#ffffff",
            foreground="#111111",
            borderwidth=1,
            relief="solid",
        )
        self.output_text.pack(fill="both", expand=True)
        self.output_text.insert("end", "Drücke eine Schaltfläche, um die Prüfungen zu starten.\n")
        self.output_text.configure(state="disabled")

    def _build_status_bar(self):
        status_frame = ttk.Frame(self, padding=(20, 10, 20, 10))
        status_frame.pack(fill="x")

        self.status_label = ttk.Label(status_frame, text="Bereit.")
        self.status_label.pack(anchor="w")

    def _set_status(self, message):
        self.status_label.config(text=message)

    def _set_buttons_state(self, state):
        for child in self.winfo_children():
            self._set_widget_state(child, state)

    def _set_widget_state(self, widget, state):
        try:
            widget.configure(state=state)
        except (tk.TclError, AttributeError):
            pass
        for child in widget.winfo_children():
            self._set_widget_state(child, state)

    def _clear_output(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")

    def _append_output(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", message)
        self.output_text.insert("end", "\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")

    def _run_task(self, task_func, title):
        self._set_status(f"{title}... Bitte warten.")
        self._set_buttons_state("disabled")
        self._clear_output()

        def worker():
            try:
                self._task_result = task_func()
                self._task_error = None
            except Exception:
                self._task_result = ""
                self._task_error = traceback.format_exc()

        self._task_thread = threading.Thread(target=worker, daemon=True)
        self._task_thread.start()
        self.after(100, self._poll_task, title)

    def _poll_task(self, title):
        if self._task_thread and self._task_thread.is_alive():
            self.after(120, self._poll_task, title)
            return

        if self._task_error:
            self._append_output("Ein Fehler ist aufgetreten:\n")
            self._append_output(self._task_error)
            self._set_status("Fehler beim Ausführen der Aufgabe.")
        else:
            self._append_output(self._task_result or f"{title} abgeschlossen.")
            self._set_status(f"{title} abgeschlossen.")

        self._set_buttons_state("normal")

    def _get_transport_id(self):
        tid = self.transport_id_entry.get().strip()
        return tid if tid else None

    def on_run_phase_1(self):
        tid = self._get_transport_id()

        def task():
            if tid:
                return run_phase_1_checks_text([tid])
            return run_phase_1_checks_text()

        self._run_task(task, "Phase 1 prüfen")

    def on_run_phase_2(self):
        self._run_task(run_phase_2_checks_text, "Phase 2 prüfen")

    def on_run_all(self):
        def task():
            parts = []
            tid = self._get_transport_id()
            if tid:
                parts.append(run_phase_1_checks_text([tid]))
            else:
                parts.append(run_phase_1_checks_text())
            parts.append(run_phase_2_checks_text())
            return "\n\n".join(parts)

        self._run_task(task, "Alle Prüfungen ausführen")

    def on_run_single_id(self):
        tid = self._get_transport_id()
        if not tid:
            self._append_output("Bitte gib eine Transport-ID ein, um sie einzeln zu prüfen.")
            self._set_status("Transport-ID erforderlich.")
            return

        def task():
            return run_phase_1_checks_text([tid])

        self._run_task(task, "Transport-ID prüfen")


if __name__ == "__main__":
    app = CoolchainApp()
    app.mainloop()     