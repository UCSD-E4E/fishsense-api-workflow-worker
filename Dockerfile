FROM ghcr.io/astral-sh/uv:python3.13-trixie AS builder

WORKDIR /app

# --- Reproduce the environment ---
# You can comment the following two lines if you prefer to manually install
# the dependencies from inside the container.
COPY pyproject.toml uv.lock /app/

# Install only the dependencies
RUN uv sync --compile-bytecode --no-dev --no-editable --no-install-project && uv cache clean

# Copy and build the package
COPY README.md /app
COPY src /app/src
RUN uv sync --compile-bytecode --no-dev --no-editable && uv cache clean

# Start building the actual runtime container.
FROM python:3.13.7-slim-trixie AS runtime

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV E4EFS_DOCKER=true

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /e4efs/config /e4efs/logs /e4efs/data /e4efs/cache

COPY --from=builder /app/.venv /app/.venv
COPY sql sql

ENTRYPOINT [ "fishsense_api_workflow_worker" ]