# Session 17 Calculator

[Complete project, workflow, security results and screenshots](../README.md)

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
gunicorn --bind 127.0.0.1:5001 app.app:app
```

Open http://localhost:5001. The calculator supports add, subtract, multiply and divide. Division by zero returns HTTP 400.
