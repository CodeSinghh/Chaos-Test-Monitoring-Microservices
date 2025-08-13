# ---------- Stage 1: Builder ----------
FROM python:3.11-alpine AS builder

LABEL maintainer="Dhiraj Singh <dhiraj.kr.singh.real@gmail.com>"
LABEL purpose="User Service for OTT Backend"
LABEL stage="build"

# Git metadata injection
ARG GIT_COMMIT=unknown
ARG VERSION=0.0.1
LABEL git_commit=$GIT_COMMIT
LABEL version=$VERSION

WORKDIR /app

# Alpine packages for build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# ---------- Stage 2: Final ----------
FROM python:3.11-alpine

LABEL maintainer="Dhiraj Singh <dhiraj.kr.singh.real@gmail.com>"
LABEL purpose="Final runtime container for User Service"

RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -S appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

USER 1001

ENV PORT=8081
ENV ENVIRONMENT=production

EXPOSE ${PORT}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
