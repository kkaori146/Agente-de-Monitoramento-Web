FROM python:3.11-slim

# Instala ping e ferramentas necessárias
RUN apt-get update && \
    apt-get install -y iputils-ping curl && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "agent.py"]
