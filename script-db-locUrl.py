import pymysql  # ou votre bibliothèque SQL
import requests

# Configuration
API_URL = "http://ip-api.com/json/"
DB_CONFIG = {
    "host": "ci-35ws9rvgbd.eba-tjt7rpak.eu-west-3.elasticbeanstalk.com",
    "user": "cowrie",
    "password": "root",
    "database": "cowrie",
}

# Connexion à la base
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# Récupérer les IP uniques
cursor.execute("SELECT DISTINCT ip FROM cowrie.sessions WHERE ip IS NOT NULL;")
ips = cursor.fetchall()

# Géolocaliser chaque IP
for ip_row in ips:
    ip = ip_row[0]
    response = requests.get(f"{API_URL}{ip}")
    data = response.json()

    if data["status"] == "success":
        latitude = data["lat"]
        longitude = data["lon"]

        print(
            f"UPDATE lat = {latitude}, long = {longitude} WHERE ip = {ip};",
        )

        # Mettre à jour la base
        cursor.execute(
            f"""
            UPDATE cowrie.sessions 
            SET lat = {latitude}, `long` = {longitude} 
            WHERE ip = '{ip}';
        """
        )
        conn.commit()

# Fermeture de la connexion
cursor.close()
conn.close()
