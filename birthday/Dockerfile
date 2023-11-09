FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py config.py database.py ./
COPY reminders.sqlite ./

CMD ["python", "main.py"]
