"""
Hilfsfunktionen für AES-Entschlüsselung der verschlüsselten Stammdaten.
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

KEY = b"mysecretpassword"
IV = b"passwort-salzen!"


def decrypt_value(encrypted_data):
    """
    Entschlüsselt einen einzelnen Datenbankwert (Bytes) mit AES-CBC.
    """
    if encrypted_data is None:
        return ""

    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted.decode("utf-8")


def load_decrypted_companies(cursor):
    """
    Liest die Tabelle company_crypt und entschlüsselt die Felder.
    """
    query = """
        SELECT companyID, company, strasse, ort, plz
        FROM dbo.company_crypt
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "companyID": row[0],
            "company": decrypt_value(row[1]),
            "strasse": decrypt_value(row[2]),
            "ort": decrypt_value(row[3]),
            "plz": decrypt_value(row[4]),
        })

    return result


def load_decrypted_transportstations(cursor):
    """
    Liest die Tabelle transportstation_crypt und entschlüsselt die Felder.

    Hinweis:
    Falls Spaltennamen in eurer DB leicht abweichen, müsst ihr das Query anpassen.
    """
    query = """
        SELECT transportstationID, transportstation, category, plz
        FROM dbo.transportstation_crypt
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "transportstationID": row[0],
            "transportstation": decrypt_value(row[1]),
            "category": decrypt_value(row[2]),
            "plz": decrypt_value(row[3]),
        })

    return result


def print_company_report(companies):
    """
    Gibt entschlüsselte Firmendaten aus.
    """
    print("\n=== Entschlüsselte Firmendaten ===")

    for c in companies:
        print(
            f"ID: {c['companyID']} | "
            f"Firma: {c['company']} | "
            f"Straße: {c['strasse']} | "
            f"Ort: {c['ort']} | "
            f"PLZ: {c['plz']}"
        )