import logging
import psycopg2
import redis as redis_client
import os
import time

from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Configure tracing
TEMPO_ENDPOINT = os.getenv("TEMPO_ENDPOINT", "http://tempo.monitoring.svc.cluster.local:4317")
provider = TracerProvider()
exporter = OTLPSpanExporter(endpoint=TEMPO_ENDPOINT, insecure=True)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    with tracer.start_as_current_span("home-handler"):
        return jsonify({
            "message": "Hello from DevOps!",
            "status": "success",
            "project": "flask-hello-devops",
            "env": os.getenv("FLASK_ENV", "dev")
        })


@app.route('/health')
def health():
    return jsonify({"status": "ok", "uptime": time.time()})


@app.route('/ready')
def ready():
    checks = {}
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), connect_timeout=2)
        conn.close()
        checks['db'] = 'ok'
    except Exception as e:
        checks['db'] = str(e)
    try:
        r = redis_client.from_url(os.getenv('REDIS_URL'), socket_connect_timeout=2)
        r.ping()
        checks['redis'] = 'ok'
    except Exception as e:
        checks['redis'] = str(e)
    all_ok = all(v == 'ok' for v in checks.values())
    status = 'ready' if all_ok else 'degraded'
    code = 200 if all_ok else 503
    return jsonify({'status': status, 'checks': checks}), code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
