"""
Datenbank-Hilfen für die Kühlkettenprüfung.

Stellt eine Leseverbindung zum MS SQL-Server her und holt Datensätze
für eine gegebene Transport-ID und Firma (nur SELECT).
"""
import pyodbc

# Verbindungsdaten wie im Aufgabenblatt vorgegeben (nur Lesezugriff).
SERVER = "sc-db-server.database.windows.net"
DATABASE = "supplychain"
USERNAME = "rse"
PASSWORD = "Pa$$w0rd"  # Im Schulkontext ok; produktiv wären Umgebungsvariablen besser.
DRIVER = "ODBC Driver 18 for SQL Server"


def get_connection():
    """Stellt eine DB-Verbindung her und gibt sie zurück."""
    conn_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}"
    )
    return pyodbc.connect(conn_str)

def load_records(company: str, transport_id: str):
    """
    Lädt alle Zeilen für Firma + Transport-ID aus dbo.coolchain.

    Rückgabe: Liste von Tupeln/Rows mit Spalten:
      company, transportid, transportstation, category, direction, datetime
    """
    # Hinweis: Spaltennamen wie im Aufgabenblatt. :contentReference[oaicite:4]{index=4}
    query = """
        SELECT company, transportid, transportstation, category, direction, [datetime]
        FROM dbo.coolchain
        WHERE company = ? AND transportid = ?
        ORDER BY [datetime] ASC
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (company, transport_id))
        return cur.fetchall()

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Verbindung erfolgreich!")
        conn.close()
    except Exception as e:
        print("❌ Fehler bei der Verbindung:", e)
