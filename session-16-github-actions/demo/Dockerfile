FROM python:3.12-alpine
WORKDIR /app
RUN adduser -D -u 10001 student
COPY app ./app
USER 10001
EXPOSE 8000
CMD ["python", "-m", "app.server"]
