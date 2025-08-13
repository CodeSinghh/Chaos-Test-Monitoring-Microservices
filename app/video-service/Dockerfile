# Stage 1: Builder
FROM python:3.11-slim AS builder
LABEL maintainer="Dhiraj Singh <dhiraj.kr.singh.real@gmail.com>"
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# Stage 2: Runner
FROM python:3.11-slim
LABEL maintainer="Dhiraj Singh <dhiraj.kr.singh.real@gmail.com>"
WORKDIR /app

# Add a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup --uid 1001 appuser

# Copy installed packages and app code
COPY --from=builder /install /usr/local
COPY . .

# Set ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER 1001

ENV PORT=8090
EXPOSE 8090

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]
