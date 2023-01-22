FROM python:3.9

WORKDIR /fastapi-mongo

COPY requirements.txt /fastapi-mongo/requirements.txt
RUN pip install -r requirements.txt

COPY . /fastapi-mongo

CMD python app/main.py