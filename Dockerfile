FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ── dependencies ──────────────────────────────────────────────────────────────
FROM base AS deps

COPY pyproject.toml .
RUN pip install --upgrade pip && \
    pip install "numpy>=2.0" "matplotlib>=3.9" "pydantic>=2.7" "pydantic-settings>=2.3"

# ── application ───────────────────────────────────────────────────────────────
FROM deps AS app

COPY src/ src/
RUN pip install --no-deps -e .

RUN mkdir -p output

# Default env — override via docker-compose or --env-file
ENV NM_PROBLEM_TYPE=ode \
    NM_PROBLEM_ID=1 \
    NM_ODE_METHOD=runge_kutta4 \
    NM_INTEGRAL_METHOD=simpson \
    NM_PDE_METHOD=explicit_euler_heat \
    NM_NUM_STEPS=10000 \
    NM_VISUALIZATION_BACKEND=file \
    NM_OUTPUT_DIR=/app/output \
    NM_FIGURE_DPI=150 \
    NM_FIGURE_FORMAT=png \
    NM_LOG_LEVEL=INFO

VOLUME ["/app/output"]

ENTRYPOINT ["python", "-m", "metodos_numericos"]

# ── test stage ────────────────────────────────────────────────────────────────
FROM app AS test

COPY tests/ tests/
RUN pip install "pytest>=8.2" "pytest-cov>=5.0"

CMD ["pytest", "--tb=short"]
