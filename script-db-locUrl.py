import pymysql  # ou votre bibliothèque SQL
import requests

# Configuration
API_URL = "http://ip-api.com/json/"
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "your_database",
}

# Connexion à la base
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# Récupérer les IP uniques
cursor.execute("SELECT DISTINCT ip FROM cowrie.downloads WHERE ip IS NOT NULL;")
ips = cursor.fetchall()

# Géolocaliser chaque IP
for ip_row in ips:
    ip = ip_row[0]
    response = requests.get(f"{API_URL}{ip}")
    data = response.json()

    if data["status"] == "success":
        latitude = data["lat"]
        longitude = data["lon"]

        # Mettre à jour la base
        cursor.execute(
            """
            UPDATE cowrie.downloads
            SET latitude = %s, longitude = %s
            WHERE ip = %s;
        """,
            (latitude, longitude, ip),
        )
        conn.commit()

# Fermeture de la connexion
cursor.close()
conn.close()
