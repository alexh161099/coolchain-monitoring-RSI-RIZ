"""
Datenbankzugriff (nur SELECT) für die Kühlkettenprüfung.
Liefert Ereignisse als (station_id, direction, datetime).
"""

import pyodbc

# Verbindungsdaten (wie im Aufgabenblatt vorgegeben)
SERVER = "sc-db-server.database.windows.net"
DATABASE = "supplychain"
USERNAME = "rse"
PASSWORD = "Pa$$w0rd"
DRIVER = "ODBC Driver 18 for SQL Server"  # falls nötig: "ODBC Driver 17 for SQL Server"

def get_connection() -> pyodbc.Connection:
    """Stellt eine DB-Verbindung her und gibt sie zurück."""
    conn_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
    )
    return pyodbc.connect(conn_str)

def load_records(company_id: int, transport_id: str):
    """
    Holt alle Ereignisse zu companyID + transportID, zeitlich aufsteigend.
    direction wird in SQL auf 'in'/'out' normalisiert (Anführungszeichen/Leerzeichen entfernt).
    Rückgabe: Liste von Tupeln (station_id, direction, datetime)
    """
    query = """
        SELECT
            ch.transportstationID AS station_id,
            LOWER(LTRIM(RTRIM(REPLACE(REPLACE(ch.direction, '''', ''), '"', '')))) AS direction,
            ch.[datetime]
        FROM dbo.coolchain AS ch
        WHERE ch.companyID = ?
          AND ch.transportID = ?
        ORDER BY ch.[datetime] ASC
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (company_id, transport_id))
        return cur.fetchall()
