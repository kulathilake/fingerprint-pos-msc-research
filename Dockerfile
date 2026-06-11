FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pos-node/ ./pos-node/
COPY feature_extractor.py .
ENV PYTHONUNBUFFERED=1
CMD ["python", "pos-node/app.py"]