FROM alpine:3.10.1

ENV APP_DIR /app
EXPOSE 8007

# app dir and user
RUN apk add --no-cache build-base bash git py3-pip openssl-dev libffi-dev python3-dev \
    && pip3 install --upgrade pip \
    && addgroup -S opinions_user \
    && adduser -S -G opinions_user opinions_user \
    && mkdir ${APP_DIR} \
    && chown -R opinions_user:opinions_user ${APP_DIR} \
    && chmod -R 770 ${APP_DIR}

WORKDIR ${APP_DIR}

USER opinions_user

ADD --chown=opinions_user:opinions_user requirements.txt ${APP_DIR}/
RUN pip3 install --user -r ${APP_DIR}/requirements.txt
ADD --chown=opinions_user:opinions_user run.py ${APP_DIR}/
ADD --chown=opinions_user:opinions_user deployment/gunicorn_logging.conf ${APP_DIR}/
ADD --chown=opinions_user:opinions_user opinions ${APP_DIR}/opinions

SHELL ["/bin/bash", "-c"]
ENTRYPOINT [ "/home/opinions_user/.local/bin/gunicorn", "-b", "0.0.0.0:8000", "--worker-tmp-dir", "/dev/shm", "--log-config", "gunicorn_logging.conf", "-w", "3", "run:app" ]
