FROM python:3.7-alpine

ENV FLASK_APP flasky
ENV FLASK_CONFIG production

WORKDIR /home/flasky

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY flasky.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]