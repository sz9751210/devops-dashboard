FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 9090

CMD ["python", "main.py"]
