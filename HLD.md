# High-Level Design (HLD) - Network Agent

## 1. Visão Geral

O **Network Agent** é um sistema para coleta, armazenamento e visualização de métricas de rede. Ele é composto por três componentes principais:

1. **Agente de Coleta**: Um serviço Python que coleta métricas de rede (como RTT, perda de pacotes, status HTTP e tempo de carregamento).
2. **Banco de Dados PostgreSQL**: Armazena as métricas coletadas.
3. **Grafana**: Interface de visualização das métricas.

O objetivo principal do sistema é monitorar a performance de hosts e serviços, fornecendo dashboards e métricas históricas para análise.

---

## 2. Componentes do Sistema

### 2.1 Network Agent (Python)
- Linguagem: Python 3.x
- Responsável por:
  - Coletar métricas de rede via ICMP e HTTP.
  - Enviar dados para o PostgreSQL.
  - Operar em container Docker.
- Arquivo principal: `agent.py`

### 2.2 Banco de Dados (PostgreSQL)
- Armazena métricas em uma tabela chamada `metrics`.
- Estrutura da tabela:

| Coluna       | Tipo                        | Descrição                   |
|------------- |---------------------------- |---------------------------- |
| id           | integer                     | Identificador único        |
| host         | text                        | Host monitorado            |
| timestamp    | timestamp without time zone | Momento da coleta          |
| avg_rtt      | double precision            | Latência média             |
| packet_loss  | double precision            | Percentual de perda        |
| http_code    | integer                     | Código HTTP da resposta    |
| load_time    | double precision            | Tempo de carregamento HTTP |

- Container Docker: `network-db`
- Porta: `5432`

### 2.3 Grafana
- Ferramenta de visualização de dashboards.
- Conectado ao PostgreSQL como fonte de dados.
- Container Docker: `network-agent-grafana-1`
- Porta: `3000`
- Dashboards configurados:
  - `network-dashboard`
- Datasource configurado: `Postgres (networkdb)`

---

## 3. Fluxo de Dados

1. O **agente Python** coleta métricas de cada host.
2. As métricas são enviadas para a tabela `metrics` do **PostgreSQL**.
3. O **Grafana** consulta o PostgreSQL e gera visualizações em dashboards.
4. Usuários acessam dashboards via navegador.

```text
[ Network Agent ] --> [ PostgreSQL ] --> [ Grafana ] --> [ Usuário ]
```

---

## 4. Infraestrutura (Docker Compose)

```yaml
version: '3'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: networkdb
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  grafana:
    image: grafana/grafana
    depends_on:
      - db
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
    restart: always

  agent:
    image: network-agent-agent
    depends_on:
      - db
    restart: always
```

---

## 5. Segurança e Configurações

- Senha do PostgreSQL: `postgres` (padrão, recomendado alterar)
- SSL desabilitado no datasource do Grafana (`sslmode: disable`)
- Acesso ao Grafana configurado via proxy.

---

## 6. Considerações de Alto Nível

- O sistema é **modular**: cada componente roda isoladamente via Docker.
- Pode ser facilmente expandido para múltiplos agentes e hosts.
- Dashboards podem ser provisionados automaticamente via YAML.
- Coleta de métricas pode ser agendada via CRON ou loop contínuo no container do agente.

---

## 7. Possíveis Extensões

- Adição de alertas no Grafana para métricas críticas.
- Suporte a TimescaleDB para métricas históricas otimizadas.
- Integração com Prometheus ou outros sistemas de monitoramento.

---

## 8. Referências

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Docker Documentation](https://docs.docker.com/)