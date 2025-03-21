FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libopencv-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5161

CMD ["python", "run.py"]