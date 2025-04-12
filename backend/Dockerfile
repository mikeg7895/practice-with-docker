FROM python:3.12.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x wait-for-it.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]