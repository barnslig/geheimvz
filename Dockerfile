FROM node:22-alpine AS app

COPY . /app

WORKDIR /app

RUN npm ci && npm run build


FROM python:3.12-alpine AS builder

RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY . /app

RUN poetry install --only main --no-root


FROM python:3.12-alpine

ARG USER_ID=3000
ARG GROUP_ID=3000

RUN apk add gettext libpq

RUN addgroup -g ${GROUP_ID} app \
    && adduser -h /app -G app -S -D -u ${USER_ID} app \
    && mkdir -p /app && chown -R app:app /app

USER app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder --chown=app:app ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=app:app . .
COPY --from=app --chown=app:app /app/core/static/core/assets /app/core/static/core/assets

RUN python manage.py compilemessages --ignore=venv
RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["daphne", "-b", "::", "-s", "'Apache/2.2.22 (Unix) PHP/5.2.0'", "geheimvz.asgi:application"]
