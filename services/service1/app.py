from flask import Flask
from prometheus_client import Counter, generate_latest, Histogram
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Application Request Latency',
    ['method', 'endpoint']
)

@app.route('/')
def index():
    start_time = time.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    return "||| 200"

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.errorhandler(404)
def page_not_found(e):
    REQUEST_COUNT.labels('GET','','404').inc()
    return "page not found"

if __name__ == '__main__':
 app.run()
