FROM python:3.9-slim

WORKDIR /fastapi-app
RUN useradd -m -r appuser && chown appuser:appuser /fastapi-app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
USER appuser
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]