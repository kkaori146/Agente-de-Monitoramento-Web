# 📡 Network Agent + ViaIpe --- Monitoramento Completo (Docker, PostgreSQL e Grafana)

🔄 Coleta automática periódica via agentes Python

📶 Testes de ping, RTT, perda de pacotes

🌍 Testes HTTP

🌐 Coleta oficial da API ViaIpe (RNP)

🧮 Cálculo de disponibilidade, banda média e qualidade dos clientes ViaIpe

🗄️ Armazenamento em dois bancos independentes (networkdb e viaipe_db)

📊 Dashboards automatizados no Grafana

🐳 Arquitetura 100% em Docker Compose

------------------------------------------------------------------------

## 📁 Estrutura do Projeto

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

------------------------------------------------------------------------

# 🎯 Objetivos do Sistema

O sistema possui **duas coletas independentes**, cada uma com seu
próprio banco e dashboard:

------------------------------------------------------------------------

## 🟦 1. Network Agent (Monitoramento de Rede)

O agente realiza periodicamente:

-   Ping\
-   Latência média (RTT)\
-   Perda de pacotes\
-   Testes HTTP (status e tempo de carregamento)

Os resultados são inseridos na tabela `metrics` no banco `networkdb`.

Dashboard: **network-dashboard.json**

------------------------------------------------------------------------

## 🟩 2. ViaIpe Agent (Coleta Oficial API RNP)

O agente acessa:

    https://legadoviaipe.rnp.br/api/norte

E gera métricas por cliente:

-   Disponibilidade\
-   Qualidade (normalizada em 0--100)\
-   Banda média (Mbps)\
-   Registro por timestamp

Os resultados são armazenados na tabela `viaipe_metrics` no banco
`viaipe_db`.

Dashboard: **viaipe-dashboard.json**

------------------------------------------------------------------------

# 🧠 Tecnologias Utilizadas

  Camada           Tecnologia
  
  ---------------- -------------------------
  
  Coleta           Python 3.11
  
  Bancos           PostgreSQL 15
  
  Visualização     Grafana
  
  Infraestrutura   Docker / Docker Compose

------------------------------------------------------------------------

# 🧱 Estrutura das Tabelas

------------------------------------------------------------------------

## 📌 Tabela `metrics` (Network Agent)

``` sql
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

------------------------------------------------------------------------

## 📌 Tabela `viaipe_metrics` (ViaIpe Agent)

``` sql
CREATE TABLE IF NOT EXISTS viaipe_metrics (
  id SERIAL PRIMARY KEY,
  client TEXT,
  timestamp TIMESTAMP,
  availability FLOAT,
  avg_bandwidth FLOAT,
  quality FLOAT
);
```

------------------------------------------------------------------------

# 🖥️ Grafana (Provisionado Automaticamente)

Acesse:

    http://localhost:3000

Login:

    admin
    admin

Dashboards carregam automaticamente via:

    grafana/provisioning/dashboards/
    grafana/provisioning/datasources/

Nenhuma configuração manual é necessária.

------------------------------------------------------------------------

# 🛠 Pré-requisitos

-   Docker\
-   Docker Compose

------------------------------------------------------------------------

# ▶️ Como Executar

### 1️⃣ Clonar o repositório

``` bash
git clone <url>
cd network-agent
```

### 2️⃣ Subir os serviços

``` bash
docker compose up --build -d
```

### 3️⃣ Verificar contêineres

``` bash
docker ps
```

### 4️⃣ Abrir o Grafana

    http://localhost:3000

------------------------------------------------------------------------

# ⚙️ Variáveis de Ambiente

## Network Agent

  Variável   Default
  
  ---------- -----------
  
  DB_HOST    db
  
  DB_NAME    networkdb
  
  DB_USER    postgres
  
  DB_PASS    postgres
  
  INTERVAL   60

## ViaIpe Agent

  Variável   Default
  
  ---------- -----------
  
  DB_HOST    db_viaipe
  
  DB_NAME    viaipe_db
  
  DB_USER    postgres
  
  DB_PASS    postgres
  
  INTERVAL   60

------------------------------------------------------------------------

# 📊 Queries Úteis

## 🔹 Verificar pasta de Queries do Projeto

------------------------------------------------------------------------

# 🧰 Comandos Úteis

## Logs

``` bash
docker compose logs -f agent
docker compose logs -f agent_viaipe
docker compose logs -f grafana
```

## Reiniciar

``` bash
docker compose down
docker compose up --build -d
```

## Acessar banco --- Network

``` bash
docker exec -it network-db psql -U postgres -d networkdb
```

## Acessar banco --- ViaIpe

``` bash
docker exec -it network-db-viaipe psql -U postgres -d viaipe_db
```

## Ver tabelas

    \dt

## Últimos registros

Network:

``` sql
SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10;
```

ViaIpe:

``` sql
SELECT * FROM viaipe_metrics ORDER BY timestamp DESC LIMIT 10;
```

------------------------------------------------------------------------

# 📚 Outros Repositórios

### Apache Airflow + Beam

https://github.com/kkaori146/Engenharia-de-Dados-Teste-Raizen

### Projeto API CO₂

https://github.com/kkaori146/Project_Airflow_API_CO2
