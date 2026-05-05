
"""
@file db.py
@brief Datenbankzugriff für die Kühlkettenprüfung.

Liest die Transportdaten aus der SQL-Server-Datenbank.
"""

import pyodbc


SERVER = "sc-db-server1.database.windows.net"
DATABASE = "supplychain"
USERNAME = "rse"
PASSWORD = "Pa$$w0rd"
DRIVER = "ODBC Driver 18 for SQL Server"


def get_connection():
    """
    @brief Erstellt eine Verbindung zur SQL-Server-Datenbank.

    @return Aktive pyodbc-Datenbankverbindung.
    """
    conn_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER},1433;"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    return pyodbc.connect(conn_str)


def load_records(company_id, transport_id):
    """
    @brief Lädt alle Kühlketteneinträge zu einer Transport-ID.

    @param company_id ID der Firma.
    @param transport_id Transport-ID.
    @return Liste mit Datensätzen (station_id, direction, datetime).
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
        cursor = conn.cursor()
        cursor.execute(query, company_id, transport_id)
        return cursor.fetchall()