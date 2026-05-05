
"""""
Datenbankzugriff für die Kühlkettenprüfung.
Liest die Transportdaten aus der SQL-Server-Datenbank.
""""


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
    """Stellt eine Verbindung zur SQL-Server-Datenbank her."""
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
    Holt alle Kühlketteneinträge zu einer Transport-ID.
    Rückgabe: Liste mit station_id, direction und datetime.
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