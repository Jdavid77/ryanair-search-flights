FROM python:3.13.3-alpine3.22 AS base

RUN apk add --no-cache gcc musl-dev

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

FROM base as build

WORKDIR /app

RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Runtime stage: copy only the virtual environment.
FROM base AS runtime

WORKDIR /app

RUN addgroup -g 1001 -S nonroot && \
    adduser -u 1001 -S nonroot -G nonroot

USER nonroot:nonroot

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=build --chown=nonroot:nonroot /app ./
COPY --chown=nonroot:nonroot ryanair ./


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

