FROM python:3.9-slim

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app"]
