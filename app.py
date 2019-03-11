from flask import Flask, request

from groupme.utils import decorators
from groupme.bot import Bot, url

app = Flask(__name__)
bot = Bot(':')

@app.route('/', methods=['POST'])
def webhook():
	return bot.webhook(data=request.get_json())

@bot.command
def test():
	print('lol cool')
	bot.send_message('Test Complete')

@bot.command
def memes():
	print('lol cool 2')
	bot.send_message('Yuyu is a big meme')