from datetime import datetime, timezone
import platform
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
started = datetime.now(timezone.utc)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/api/status")
def status():
    return jsonify(status="running", python_version=platform.python_version(),
                   uptime=str(datetime.now(timezone.utc) - started))


@app.get("/api/greet/<name>")
def greet(name):
    return jsonify(message=f"Hello, {name}!", name=name)


@app.post("/api/add")
def add():
    data = request.get_json() or {}
    try:
        result = float(data["number1"]) + float(data["number2"])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="Both numbers are required"), 400
    return jsonify(result=result)


@app.post("/api/calculate")
def calculate():
    data = request.get_json() or {}
    try:
        a, b = float(data["a"]), float(data["b"])
        operation = data.get("operation", "add")
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            result = a / b
        else:
            return jsonify(error="Unknown operation"), 400
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return jsonify(error="Valid numbers and a nonzero divisor are required"), 400
    return jsonify(result=result)
