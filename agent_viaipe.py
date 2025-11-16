import requests
import time
import psycopg2
from datetime import datetime
import os

# Configurações do banco (variáveis de ambiente)
DB_HOST = os.getenv("DB_HOST", "db_viaipe")
DB_NAME = os.getenv("DB_NAME", "viaipe_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
INTERVAL = int(os.getenv("INTERVAL", "60"))

API_URL = "https://legadoviaipe.rnp.br/api/norte"

def connect_db():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME,
        user=DB_USER, password=DB_PASS
    )

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS viaipe_metrics (
            id SERIAL PRIMARY KEY,
            client TEXT,
            timestamp TIMESTAMP,
            availability FLOAT,
            avg_bandwidth FLOAT,
            quality FLOAT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def fetch_data():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()
        return data
    except Exception as e:
        print(f"Erro ao consumir API: {e}")
        return []

def calculate_metrics(site_data):
    """
    Calcula métricas agregadas para cada site/cliente
    - Disponibilidade média
    - Consumo médio de banda
    - Qualidade (exemplo: max_out / capacidade teórica)
    """
    interfaces = site_data.get("data", {}).get("interfaces", [])
    if not interfaces:
        return 0, 0, 0

    total_availability = 0
    total_bandwidth = 0
    total_quality = 0
    count = len(interfaces)

    for iface in interfaces:
        # Exemplo: disponibilidade como 100% se max_out > 0
        availability = 100 if iface.get("max_out", 0) > 0 else 0
        avg_in = iface.get("avg_in", 0)
        avg_out = iface.get("avg_out", 0)
        max_out = iface.get("max_out", 0)

        bandwidth = (avg_in + avg_out) / 2
        quality = (bandwidth / max_out * 100) if max_out > 0 else 0

        total_availability += availability
        total_bandwidth += bandwidth
        total_quality += quality

    # Retorna médias
    return total_availability / count, total_bandwidth / count, total_quality / count

def save_metric(client, availability, avg_bandwidth, quality):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO viaipe_metrics (client, timestamp, availability, avg_bandwidth, quality)
            VALUES (%s, %s, %s, %s, %s);
        """, (client, datetime.utcnow(), availability, avg_bandwidth, quality))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")

def main():
    init_db()
    print("🚀 Agente ViaIpe iniciado...")

    while True:
        sites_data = fetch_data()
        for site_data in sites_data:
            client_name = site_data.get("nome", site_data.get("lat", "unknown"))
            availability, avg_bandwidth, quality = calculate_metrics(site_data)
            save_metric(client_name, availability, avg_bandwidth, quality)
            print(f"{datetime.utcnow()} | {client_name} | availability={availability:.2f} | bandwidth={avg_bandwidth:.2f} | quality={quality:.2f}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
