import subprocess
import requests
import time
import psycopg2
from datetime import datetime
import os

hosts = ["google.com", "youtube.com", "rnp.br"]

# Configurações do banco (variáveis de ambiente)
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "networkdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

INTERVAL = int(os.getenv("INTERVAL", "60"))


def connect_db():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME,
        user=DB_USER, password=DB_PASS
    )


def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id SERIAL PRIMARY KEY,
            host TEXT,
            timestamp TIMESTAMP,
            avg_rtt FLOAT,
            packet_loss FLOAT,
            http_code INT,
            load_time FLOAT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def ping_host(host):
    try:
        result = subprocess.run(
            ["ping", "-c", "4", host],
            capture_output=True,
            text=True
        )
        output = result.stdout

        if not output or "packet loss" not in output:
            return None, None

        # Perda de pacotes
        loss_line = [l for l in output.splitlines() if "packet loss" in l][0]
        packet_loss = float(loss_line.split(",")[2].split("%")[0].strip())

        # RTT médio
        rtt_line = [l for l in output.splitlines() if "rtt min/avg/max" in l]
        if rtt_line:
            avg_rtt = float(rtt_line[0].split("=")[1].split("/")[1])
        else:
            avg_rtt = None

        return avg_rtt, packet_loss

    except Exception as e:
        print(f"Erro no ping de {host}: {e}")
        return None, None


def test_http(host):
    try:
        start = time.time()
        response = requests.get(f"https://{host}", timeout=10)
        load_time = time.time() - start
        return load_time, response.status_code

    except Exception as e:
        print(f"Erro HTTP em {host}: {e}")
        return None, None


def save_metric(host, avg_rtt, packet_loss, http_code, load_time):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO metrics (host, timestamp, avg_rtt, packet_loss, http_code, load_time)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (host, datetime.utcnow(), avg_rtt, packet_loss, http_code, load_time))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")


def main():
    init_db()
    print("📡 Network agent iniciado...")

    while True:
        for host in hosts:
            avg_rtt, packet_loss = ping_host(host)
            load_time, http_code = test_http(host)
            save_metric(host, avg_rtt, packet_loss, http_code, load_time)

            print(
                f"{datetime.utcnow()} | {host} | ping={avg_rtt}ms | loss={packet_loss}% "
                f"| HTTP={http_code} | load={load_time}s"
            )

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
