FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY browniereq.txt browniereq.txt
RUN pip install -r browniereq.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]