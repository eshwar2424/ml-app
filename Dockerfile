FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY train.py .
COPY app.py .

RUN python train.py

EXPOSE 5000

CMD ["python", "app.py"]
