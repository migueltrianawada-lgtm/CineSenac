FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CINESENAC_SECRET_KEY=container-test-only-secret

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY cine_senac ./cine_senac

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "cine_senac:create_app()", "run", "--host=0.0.0.0", "--port=5000"]
