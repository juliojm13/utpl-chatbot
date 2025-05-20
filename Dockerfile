FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code

CMD ["uvicorn", "app.interface.main:app", "--host", "0.0.0.0", "--port", "8000"] 