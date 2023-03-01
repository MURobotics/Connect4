FROM python:latest

WORKDIR /usr/app/src

COPY connect_four_terminal.py ./

RUN pip install numpy

CMD ["python", "./connect_four_terminal.py"]