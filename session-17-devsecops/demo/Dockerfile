FROM python:3.12-alpine
WORKDIR /app
RUN adduser -D -u 10001 student
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
USER 10001
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app.app:app"]
