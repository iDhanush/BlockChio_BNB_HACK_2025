FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed for brownie
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libgmp-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install eth-brownie (should not be in CMD)
RUN pip install eth-brownie

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
