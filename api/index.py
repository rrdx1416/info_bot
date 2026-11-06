import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"
REPLY = "Ваш текст сообщения"


def tg(method, data):
    req = urllib.request.Request(
        f"{API}/{method}",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
    )
    return urllib.request.urlopen(req).read()


class handler(BaseHTTPRequestHandler):
    # Открываете https://ВАШ-ПРОЕКТ.vercel.app/api/
    # в браузере, и webhook ставится
    def do_GET(self):
        host = self.headers["Host"]
        res = tg("setWebhook", {"url": f"https://{host}/api/"})
        self.send_response(200)
        self.end_headers()
        self.wfile.write(res)

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        update = json.loads(body)
        msg = update.get("message")
        if msg:
            tg("sendMessage", {"chat_id": msg["chat"]["id"], "text": REPLY})
        self.send_response(200)
        self.end_headers()
