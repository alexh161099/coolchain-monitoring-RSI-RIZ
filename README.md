# coolchain-monitoring-RSE.

Der Hersteller **„Food Solution Hildesheim“** produziert Bio-Dönerspieße und bietet eine zertifizierte Kühlkette an.
Die Einhaltung kann vom Endkunden über einen **QR-Code** überprüft werden.

---

## Kühlkettenüberwachung

Dieses Python-Programm überprüft für vorgegebene Transport-IDs die Einhaltung der Kühlkette.

---

## Projektphase 1

Das Programm prüft folgende Kriterien:

* **Stimmigkeit je Station**

  * Jede Station besitzt ein Ein- und Auschecken
  * Reihenfolge: `in → out`

* **Übergaben ohne Kühlung**

  * Maximal **10 Minuten** zwischen zwei Stationen

* **Gesamttransportdauer**

  * Maximal **48 Stunden**

---

## Projektphase 2 (Erweiterung)

### Temperaturüberwachung

* Auswertung der Tabelle `tempdata`
* Gültiger Bereich: **+2 °C bis +4 °C**
* Ausgabe von Temperaturabweichungen

---

### Entschlüsselung der Daten

* Tabellen:

  * `company_crypt`
  * `transportstation_crypt`
* Verschlüsselung: **AES (CBC Mode)**

---

### Wetterdaten bei Übergabefehlern

* Bei Überschreitung der Übergabezeit wird die Außentemperatur abgefragt
* Datenquelle: **Visual Crossing API**
* Ausgabe direkt in der Fehlermeldung

---

## Voraussetzungen

* Windows
* Python 3.12
* Microsoft ODBC Driver 17 oder 18 für SQL Server

---

## Verwendung

1. In `src/main.py` die **Company-ID prüfen/anpassen**
2. Programm starten:

```bash
python src/main.py
```

---

## Ausgabe

* Für jede Transport-ID: **OK / FAIL**
* Bei Fehlern: **klare Begründung**
* Bei Übergabefehlern: zusätzliche **Wetterinformation**

---

## Start

* Doppelklick auf `Start_Kuehlkette.bat`
  oder
* Start über VS Code / Terminal

---

## Beispielausgabe

```text
OK   ID 72359278599178561029675: Kühlkette eingehalten
FAIL ID 15668407856331648336231: Übergabe: > 10 min | Wetter: 6 °C
```
