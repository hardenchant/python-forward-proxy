FROM python

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
