# coolchain-monitoring-RSE.

Der Hersteller **„Food Solution Hildesheim“** produziert Bio-Dönerspieße und bietet eine zertifizierte Kühlkette an.
Die Einhaltung kann vom Endkunden über einen **QR-Code** überprüft werden.
Das Projekt wurde durchgeführt von Alexander Holzenkamp, Fynn Bremer und Tom Stoelken.

#  IoT-Kühlkettenüberwachung

Dieses Projekt überprüft automatisiert die Einhaltung einer Kühlkette für Transportprozesse.
Die Auswertung erfolgt anhand von Daten aus einer SQL-Server-Datenbank.

Der Endkunde kann die Kühlkette über eine Transport-ID (z. B. per QR-Code) nachvollziehen.

---

## Projektübersicht

Das Programm besteht aus zwei Projektphasen:

### Projektphase 1 – Grundprüfung

* Prüfung der **Stimmigkeit je Station**

  * Jede Station muss ein `in` und ein `out` besitzen
  * Reihenfolge: `in → out`

* Prüfung der **Übergabezeiten**

  * Maximal **10 Minuten** zwischen zwei Stationen

* Prüfung der **Transportdauer**

  * Maximal **48 Stunden**

---

###  Projektphase 2 – Erweiterungen

#### Temperaturüberwachung

* Auswertung der Tabelle `tempdata`
* Erlaubter Bereich: **+2 °C bis +4 °C**
* Ausgabe aller Temperaturverstöße

#### Entschlüsselung von Firmendaten

* Tabellen:

  * `company_crypt`
  * `transportstation_crypt`
* Verschlüsselung: **AES (CBC Mode)**

#### Wetterdatenintegration

* Bei Übergabefehlern wird die Außentemperatur abgefragt
* Datenquelle: **Visual Crossing Weather API**
* Ausgabe direkt in der Fehlermeldung

---

## Voraussetzungen

* Windows
* Python 3.12
* Microsoft ODBC Driver 17 oder 18 für SQL Server
* Internetverbindung (für Wetterdaten)

---

## Installation

1. Repository klonen:

```bash
git clone https://github.com/DEIN-REPO
cd coolchain-monitoring
```

2. Python-Abhängigkeiten installieren:

```bash
pip install requests pyodbc
```

3. ODBC-Treiber installieren:
   👉 https://learn.microsoft.com/de-de/sql/connect/odbc/download-odbc-driver-for-sql-server

---

## API-Key einrichten

Für die Wetterdaten wird ein API-Key benötigt:

👉 https://www.visualcrossing.com/weather-api

Den Key in `weather.py` eintragen:

```python
API_KEY = "DEIN_API_KEY"
```

---

## Programm starten

### Variante 1 (Konsole)

```bash
python src/main.py
```

### Variante 2 (GUI)

```bash
python src/main.py
```

→ startet automatisch die grafische Oberfläche

---

## Alternative: Start über EXE / Batch

Das Programm kann auch einfach über die bereitgestellte Startdatei ausgeführt werden:

```text
Start_Kuehlkette.bat
```

→ kein Python-Know-how notwendig

---

## Bedienung

* **Phase 1 prüfen** → Grundprüfung
* **Phase 2 prüfen** → Erweiterungen
* **Alle prüfen** → komplette Auswertung
* **Transport-ID eingeben** → gezielte Prüfung

Die grafische Oberfläche ist intuitiv bedienbar und zeigt die Ergebnisse übersichtlich an.

---

## Ausgabe

Beispiel:

```text
OK   ID 72359278599178561029675: Kühlkette eingehalten.
FAIL ID 15668407856331648336231: Übergabe > 10 min: 11 min | Wetter: 16.6 °C
```

---

##  Programmablauf

1. Daten werden aus der SQL-Datenbank geladen (`db.py`)
2. Prüfung erfolgt in Modulen (`checks.py`)
3. Erweiterungen:

   * Temperaturprüfung (`temperature.py`)
   * Entschlüsselung (`crypto_utils.py`)
   * Wetterdaten (`weather.py`)
4. Ausgabe erfolgt:

   * in der Konsole
   * oder über die GUI (Tkinter)

---

##  Projektstruktur

```text
src/
│── main.py              → Hauptprogramm + GUI
│── db.py                → Datenbankzugriff
│── checks.py            → Prüfalgorithmen
│── temperature.py       → Temperaturprüfung
│── weather.py           → Wetter-API
│── crypto_utils.py      → Entschlüsselung
```

---

## Fehlerbehandlung

Das Programm ist fehlertolerant und erkennt u. a.:

* unbekannte Transport-IDs
* doppelte Richtungen (`out → out`)
* fehlende Datenbankeinträge
* Datenbankfehler
* API-Ausfälle (z. B. Limit erreicht)

Fehlermeldungen sind eindeutig und verständlich formuliert.

---

##  Team

* Fynn Bremer
* Alexander Holzenkamp
* Tom Stoelken
