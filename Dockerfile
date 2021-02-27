# Build all required packages
FROM python:3.8.1-alpine as base
ARG POETRY_EXPORT_ARGS
WORKDIR /src
COPY . /src

RUN apk add --no-cache --virtual .build-dependencies gcc build-base libffi-dev openssl-dev

RUN pip install poetry

RUN poetry build -f wheel
RUN poetry export $POETRY_EXPORT_ARGS --without-hashes -f requirements.txt -o requirements.txt
RUN cat requirements.txt | grep -v 'sys_platform == "win32"' | xargs -I{} pip wheel -w ./wheels {}

# Live stage
FROM python:3.8.1-alpine
RUN adduser -D -h /app -u 1000 app

RUN apk add --no-cache git

COPY --from=base /src/requirements.txt /src/wheels /src/dist/*.whl /app/
RUN pip install --find-links=/app -r /app/requirements.txt /app/flox*-py3-none-any.whl

# Clean up
RUN rm -rf /app

ENTRYPOINT ["flox"]
