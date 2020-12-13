FROM python:3.7.3
WORKDIR /project
ADD . /project

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install libopenblas-dev
RUN apt-get -y install libomp-dev
RUN pip install --upgrade pip

CMD ["python","src/server.py"]
