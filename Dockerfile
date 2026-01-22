FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set python path
ENV PYTHONPATH=/app

# Run the bot
CMD ["python", "src/bot.py"]
