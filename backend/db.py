import mysql.connector
import os

def conectar():
    return mysql.connector.connect(
        host=os.environ.get("margaradb-aioria123.e.aivencloud.com"),
        user=os.environ.get("avnadmin"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("defaultdb"),
        port=os.environ.get("16443") # Usamos el puerto de Aiven
    )