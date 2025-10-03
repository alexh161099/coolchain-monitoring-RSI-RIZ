# coolchain-monitoring-RSI-RIZ
Der Hersteller „Food Solution Hildesheim“ produziert Bio-Dönerspieße. Er bietet seinen Endkunden eine zertifizierte Kühlkette für alle Produkte an. Die Einhaltung der Kühlkette kann vom Endkunden leicht über einen QR-Code überprüft werden. 
# Kühlkettenüberwachung

Dieses Programm prüft für vorgegebene Transport-IDs drei Kriterien:
1) Stimmigkeit je Station (Reihenfolge in → out)
2) Übergaben ohne Kühlung ≤ 10 Minuten
3) Gesamttransportdauer ≤ 48 Stunden

## Voraussetzungen
- Windows, Python 3.12
- Microsoft ODBC Driver 18 for SQL Server (oder 17)
- Python-Paket: pyodbc

## Verbindung (vorgegeben)
Server: sc-db-server.database.windows.net  
Datenbank: supplychain  
Benutzer: rse / Passwort: Pa$$w0rd  
Company-ID: 1703

## Verwendung
- In `src/main.py` COMPANY_ID anpassen (z. B. 1703).  
- `src/main.py` starten (VS Code ►).
- Ausgabe: Für jede Transport-ID „OK“ oder „FAIL“ mit Begründung.
- Hinweis: Es wird bewusst der **erste** festgestellte Verstoß ausgegeben.

## Start
- Doppelklick auf `Start_Kuehlkette.bat`
- Ausgabe: pro Transport-ID „OK/FAIL + eindeutige Begründung“
- Hinweis: Es wird jeweils der **erste** festgestellte Verstoß gemeldet.

## Dokumentation
Die automatisch erzeugte HTML-Dokumentation liegt unter `docs/html/index.html`.
