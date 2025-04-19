FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python dependencies with verbose output
RUN pip install --verbose --no-cache-dir -r requirements.txt
RUN pip install --verbose --no-cache-dir python-chess==1.2.0
RUN pip list | grep chess
RUN python -c "import chess; print(f'Chess module imported successfully')"
RUN python -c "import chess; print(f'Chess module attributes: {[attr for attr in dir(chess) if not attr.startswith(\"__\")]}')"
RUN python -c "import sys; print(f'Python path: {sys.path}')"

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
