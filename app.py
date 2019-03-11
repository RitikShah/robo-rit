from flask import Flask, request

from groupme.utils import decorators
from groupme.bot import Bot, url

app = Flask(__name__)
bot = Bot()

@decorators.debug
@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	bot.webhook(data=data)

@decorators.debug
@bot.command
def test():
	print('lol cool')
	bot.send_message('Success!')

@decorators.debug
@bot.listener
def test2(msg):
	print(msg)
	bot.send_message(f'HELP ME YUYU {msg}')