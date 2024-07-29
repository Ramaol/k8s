from flask import Flask, request
from prometheus_client import Counter, generate_latest, Histogram
import time, os, asyncio, telegram 


TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Telegram Alert Latency',
    ['method', 'endpoint']
)

async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)

def format_json(text):
    result = f"reciever: {text['receiver']}\n\
status: {text['status']}\n\
alert-name: {text['alerts'][0]['labels']['alertname']}\n\
prometheus: {text['alerts'][0]['labels']['prometheus']}\n\
message: {text['alerts'][0]['annotations']['message']}\n\
startsAt: {text['alerts'][0]['startsAt']}\n\
endAt: {text['alerts'][0]['endsAt']}"
    
    return result

@app.route('/', methods=['POST'])
def index():
    start_time = time.time()
    REQUEST_COUNT.labels('POST', '/', 200).inc()
    request_data = request.get_json()
    print(request_data)
    asyncio.run((send_message(format_json(request_data), CHAT_ID)))
    REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    return f"{request_data}"

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
 app.run()

