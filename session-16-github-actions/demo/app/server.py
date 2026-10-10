from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs, urlparse
from app.calculator import add, subtract, multiply, divide


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path)
        if path.path == "/health":
            payload = {"status": "healthy"}
        elif path.path == "/api/calculate":
            params = parse_qs(path.query)
            try:
                a, b = float(params["a"][0]), float(params["b"][0])
                operation = params.get("operation", ["add"])[0]
                result = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}[operation](a, b)
                payload = {"result": result}
            except (KeyError, ValueError, ZeroDivisionError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid calculation")
                return
        else:
            payload = {"application": "Session 16 calculator", "example": "/api/calculate?a=6&b=3&operation=multiply"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
