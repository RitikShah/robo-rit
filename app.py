from flask import Flask, request

from groupme.utils import decorators
from groupme.bot import Bot, url

app = Flask(__name__)
bot = Bot()

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	return bot.webhook(data=data)

@bot.command
def test():
	print('lol cool')
	bot.send_message('Success!')

@bot.listener
def test2(msg):
	print(msg['text'])
	bot.send_message(f"HELP ME YUYU {msg['text']}")