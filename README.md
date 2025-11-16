# 📡 Network Agent – Monitoramento de Rede com Docker, PostgreSQL e Grafana

sistema para **monitoramento de desempenho de rede**, incluindo:

- 🔄 **Coleta automática periódica** via agente Python
- 📶 Testes de rede (ping, latência, perda de pacotes)
- 🌍 Testes HTTP (tempo de carregamento e códigos de resposta)
- 🗄️ Armazenamento em banco PostgreSQL
- 📊 Visualização no Grafana com dashboards provisionados
- 🐳 orquestração realizado 100% com Docker Compose

---

## 📁 Estrutura do Repositório

```
network-agent/
├── agent.py
├── agent_viaipe.py
├── Dockerfile
├── Dockerfile_viaipe
├── docker-compose.yml
├── requirements.txt
└── grafana/
    └── provisioning/
        ├── datasources/
        │   ├── datasource.yml
        │   ├── datasource_viaipe.yml
        └── dashboards/
            ├── dashboard-provider.yml
            ├── network-dashboard.json
            └── viaipe-dashboard.json
```

---

## 🚀 Objetivo do Projeto

Construir uma solução simples e portátil para monitoramento de rede capaz de:

- Medir conectividade com hosts externos
- Armazenar as métricas em banco de dados
- Exibir dashboards automaticamente no Grafana
- Funcionar em qualquer ambiente via Docker

Hosts monitorados:

- `google.com`
- `youtube.com`
- `rnp.br`

---

## 🧠 Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|------------|
| Coleta de dados | Python 3.11 |
| Banco de dados | PostgreSQL 15 |
| Visualização | Grafana |
| Infraestrutura | Docker & Docker Compose |

---

## 🧱 Componentes

### 🔹 **Agent (Python)**
Realiza periodicamente:
- Ping (média RTT e % perda)
- Requisição HTTP + tempo de resposta + status HTTP

Valores são inseridos na tabela `metrics` no PostgreSQL.

### 🔹 **PostgreSQL**
Estrutura da tabela:

```sql
CREATE TABLE IF NOT EXISTS metrics (
  id SERIAL PRIMARY KEY,
  host TEXT,
  timestamp TIMESTAMP,
  avg_rtt FLOAT,
  packet_loss FLOAT,
  http_code INT,
  load_time FLOAT
);
```

### 🔹 **Grafana**
- Datasource provisionado automaticamente
- Dashboard criado via JSON
- Nenhuma configuração manual necessária

Acesse em:
```
http://localhost:3000
```

Login:  
`admin / admin`

---

## 🛠 Pré-requisitos

- Docker Desktop instalado
- Docker Compose

---

# ▶️ Como Rodar o Projeto

### 1️⃣ Clonar o repositório
```bash
git clone <url>
cd network-agent
```

### 2️⃣ Subir os containers
```bash
docker compose up --build -d
```

### 3️⃣ Verificar que os serviços estão rodando
```bash
docker ps
```

### 4️⃣ Acessar o Grafana
```
http://localhost:3000
```

Login: **admin / admin**

---

# ⚙️ Variáveis de Ambiente

### Agent
| Variável | Descrição | Default |
|----------|-----------|---------|
| `DB_HOST` | Host do Postgres | db |
| `DB_NAME` | Nome do banco | networkdb |
| `DB_USER` | Usuário | postgres |
| `DB_PASS` | Senha | postgres |
| `INTERVAL` | Intervalo de coleta (s) | 60 |

### PostgreSQL
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

---

# 📈 Dashboard

O dashboard mostra:

- Latência média por host
- Perda de pacotes
- Tempo HTTP
- Últimos códigos de retorno por site

A query usada nos gráficos:

```sql
SELECT
  timestamp AS "time",
  avg_rtt
FROM metrics
WHERE $__timeFilter(timestamp)
ORDER BY timestamp;
```

---

# 🧰 Comandos Úteis

### Logs
```bash
docker compose logs -f agent
docker compose logs -f db
docker compose logs -f grafana
```

### Restart
```bash
docker compose down
docker compose up --build -d
```

### Acessar banco
```bash
docker exec -it network-db psql -U postgres -d networkdb
```

### Ver tabela
```sql
\dt
```

### Ver dados
```sql
SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10;
```

----------------------------------------------------------------
# Repositórios Extras Indicados:

## Projeto com Apache Airflow e Apache Beam
https://github.com/kkaori146/Engenharia-de-Dados-Teste-Raizen

## Projeto com API
https://github.com/kkaori146/Project_Airflow_API_CO2