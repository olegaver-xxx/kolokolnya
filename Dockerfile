FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    APP_PATH=/app

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#RUN #apt update && \
#    apt install python3-pip -y && \
#    pip install -U pip && \
#    pip install poetry -y

WORKDIR $APP_PATH
COPY pyproject.toml $APP_PATH/
COPY poetry.lock $APP_PATH/
RUN poetry export -f requirements.txt --output $APP_PATH/requirements.txt --without-hashes
RUN pip install -r requirements.txt
COPY ./src $APP_PATH/

ENTRYPOINT ["/app/entrypoint.sh"]
