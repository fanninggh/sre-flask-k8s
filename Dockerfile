FROM python:3.12-alpine AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-alpine
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
RUN apk upgrade --no-cache
COPY --from=builder /install /usr/local
COPY --chown=app:app app.py .
USER app
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:5000/health || exit 1
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
