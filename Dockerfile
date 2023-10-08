FROM python:3.12-slim

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
