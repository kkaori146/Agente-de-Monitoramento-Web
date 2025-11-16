# High-Level Design (HLD) – Network Agent + ViaIPE Agent

## 1. Visão Geral

Este sistema é composto por **dois agentes independentes**, cada um responsável por coletar métricas diferentes:

### **1. Network Agent**
Coleta métricas de rede:
- Latência (RTT)
- Perda de pacotes
- Tempo de carregamento HTTP
- Código HTTP

### **2. ViaIPE Agent**
Coleta métricas de clientes do ViaIPE:
- Disponibilidade
- Consumo de banda

Cada agente envia os dados para bancos PostgreSQL separados.  
O Grafana exibe dashboards automáticos a partir desses bancos.

---

## 2. Componentes do Sistema

### **2.1 Network Agent (Python)**

Arquivo: `agent.py`  
Responsabilidades:
- Envia pings periódicos
- Executa testes HTTP
- Insere métricas no banco `networkdb`

**Estrutura da tabela `metrics`:**

| Coluna       | Tipo       |
|--------------|------------|
| id           | SERIAL     |
| host         | TEXT       |
| timestamp    | TIMESTAMP  |
| avg_rtt      | FLOAT      |
| packet_loss  | FLOAT      |
| http_code    | INT        |
| load_time    | FLOAT      |

---

### **2.2 ViaIPE Agent (Python)**

Arquivo: `agent_viaipe.py`  
Responsabilidades:
- Coletas de disponibilidade
- Consumo de banda
- Inserção no banco `viaipe_db`

**Estrutura da tabela `viaipe_metrics`:**

| Coluna         | Tipo       |
|----------------|------------|
| id             | SERIAL     |
| client         | TEXT       |
| timestamp      | TIMESTAMP  |
| availability   | FLOAT      |
| avg_bandwidth  | FLOAT      |

---

### **2.3 Bancos PostgreSQL**

Dois bancos separados:

| Serviço | Banco         | Tabela            |
|--------|---------------|--------------------|
| Network Agent | `networkdb` | `metrics` |
| ViaIPE Agent | `viaipe_db` | `viaipe_metrics` |

---

### **2.4 Grafana**

- Porta: **3000**
- Provisionamento automático
- Dashboards:
  - `network-dashboard.json`
  - `viaipe-dashboard.json`
- Datasources:
  - PostgreSQL – Network
  - PostgreSQL – ViaIPE

---

## 3. Fluxo de Dados

[ Network Agent ] ---> [ PostgreSQL networkdb ] ---> [ Grafana ] ---> Usuário

[ ViaIPE Agent ] ---> [ PostgreSQL viaipe_db ] ---> [ Grafana ] ---> Usuário


---

## 4. Infraestrutura Docker

Todos os serviços são orquestrados por Docker Compose:

- 2 bancos PostgreSQL
- 2 agentes Python
- Grafana com provisioning automático
- Volumes persistentes para bancos
- Reinício automático (`restart: always`)

---

## 5. Segurança e Configurações

Credenciais padrão do PostgreSQL (recomendado mudar)

Sem SSL (rede interna Docker)

Volumes persistentes

Grafana provisionado automaticamente via JSON e YAML

---

## 6. Referências

Documentação do PostgreSQL

Documentação do Grafana

Documentação do Docker