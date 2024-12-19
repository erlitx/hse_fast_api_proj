# Use an official Python base image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app/data

WORKDIR $APP_HOME

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 80

VOLUME /app/data
# Start FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
