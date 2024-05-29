FROM python:3.12.3-alpine3.20

ENV PROJECT_NAME=my-study-api
ENV POSTGRES_HOST=postgres_db
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER=main-user
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydatabase
ENV ENVIRONMENT=local
ENV BACKEND_CORS_ORIGINS="http://localhost,http://localhost:5173,https://localhost,https://localhost:5173,http://localhost.tiangolo.com"

RUN apk update && apk add --no-cache libpq gcc musl-dev postgresql-dev

RUN pip install poetry
RUN apk update && apk add --no-cache \
    build-base \
    htop \
    tzdata

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install

ADD . /app/

EXPOSE 9000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
