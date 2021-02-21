FROM python:3

MAINTAINER Olivia Li

RUN apt-get update -y && apt-get install -y python3-pip

EXPOSE 80
EXPOSE 5000

WORKDIR /museum_analysis

COPY ./requirements.txt /museum_analysis

RUN pip3 install -r requirements.txt

COPY . /museum_analysis

ENTRYPOINT ["python3"]

CMD ["main.py"]