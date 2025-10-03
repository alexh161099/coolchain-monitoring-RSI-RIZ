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
DB: supplychain  
User: rse / Passwort: Pa$$w0rd

## Verwendung
- In `src/main.py` COMPANY_ID anpassen (z. B. 1703).  
- `src/main.py` starten (VS Code ►).
- Ausgabe: Für jede Transport-ID „OK“ oder „FAIL“ mit Begründung.
- Hinweis: Es wird bewusst der **erste** festgestellte Verstoß ausgegeben.
