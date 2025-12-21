FROM python:3.10-slim-bookworm

WORKDIR /app
COPY . /app

# Install AWS CLI (v1 from Debian repos) + any basic OS deps you may need
RUN apt-get update && apt-get install -y --no-install-recommends awscli \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
