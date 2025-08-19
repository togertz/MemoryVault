FROM python:3.13-slim

WORKDIR /

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /src/memoryvault/ /src/memoryvault
COPY app.py .

CMD ["python", "app.py"]
