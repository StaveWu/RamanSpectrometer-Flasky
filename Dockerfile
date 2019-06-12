FROM python:3.7.3

ENV FLASK_APP flasky
ENV FLASK_CONFIG production

WORKDIR /home/flasky

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY flasky.py config.py reset.py boot.sh ./
RUN python reset.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]