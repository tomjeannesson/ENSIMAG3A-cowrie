import json

import pymysql

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
cursor.execute("SELECT DISTINCT domain FROM cowrie.sessions WHERE domain IS NOT NULL;")
domains = cursor.fetchall()
cursor.execute("SELECT DISTINCT input FROM cowrie.input")
inputs = cursor.fetchall()

with open("db-save.json", "w") as f:
    json.dump(
        {
            "domains": [domain[0] for domain in domains],
            "inputs": [input[0] for input in inputs],
        },
        f,
        indent=4,
    )
cursor.close()
conn.close()
