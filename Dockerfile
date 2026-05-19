FROM python:3.11-slim

LABEL maintainer="Kartik Chhabra"
LABEL project="PH4NT0M"
LABEL description="Advanced JavaScript Recon & Secret Intelligence Framework"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m ph4nt0m

USER ph4nt0m

ENTRYPOINT ["python3", "ph4nt0m.py"]
