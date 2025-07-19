FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed for brownie and git
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libgmp-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone membase repo and install it
RUN git clone https://github.com/iDhanush/membase.git && \
    cd membase && \
    pip install -e .

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install brownie and configure BSC testnet
RUN pip install eth-brownie && \
    brownie networks add BinanceSmartChain bsc-testnet host=https://bsc-testnet-dataseed.bnbchain.org chainid=97 explorer=https://testnet.bscscan.com

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
