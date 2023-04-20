FROM python:3.10-alpine

RUN mkdir /app

WORKDIR /app

COPY . /app

# RUN apk add --no-cache py3-pip

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start_spiders.sh

CMD ["./start_spiders.sh"]
