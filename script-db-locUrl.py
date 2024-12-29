import socket
from time import sleep

import pymysql
import requests

API_URL = "http://ip-api.com/json/"
DB_CONFIG = {
    "host": "ci-35ws9rvgbd.eba-tjt7rpak.eu-west-3.elasticbeanstalk.com",
    "user": "cowrie",
    "password": "root",
    "database": "cowrie",
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute(
    "SELECT DISTINCT ip FROM cowrie.sessions WHERE ip IS NOT NULL AND domain IS NULL AND seen = FALSE;"
)
ips = cursor.fetchall()

for index, ip_row in enumerate(ips):
    ip = ip_row[0]
    success = False
    while not success:
        try:
            response = requests.get(f"{API_URL}{ip}")
            data = response.json()
            success = True
        except requests.exceptions.JSONDecodeError:
            print("An error occurred, retrying in 1s.")
            sleep(1)

    if data["status"] == "success":
        latitude = data["lat"]
        longitude = data["lon"]
        domain = socket.getnameinfo((ip, 0), 0)[0]

        print(
            f"{index}/{len(ips)} UPDATE lat = {latitude}, long = {longitude}, domain = {domain} WHERE ip = {ip} AND ip != '{domain}';"
        )

        cursor.execute(
            f"""
            UPDATE cowrie.sessions 
            SET lat = {latitude}, `long` = {longitude}, `domain` = '{domain}'
            WHERE ip = '{ip}' AND ip != '{domain}';
        """
        )
        conn.commit()
        cursor.execute(
            f"""
            UPDATE cowrie.sessions 
            SET `seen`= TRUE
            WHERE ip = '{ip}';
        """
        )
        conn.commit()

cursor.close()
conn.close()
