FROM python:3

WORKDIR /home/ben/snappy-api

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "wsgi.py" ]

