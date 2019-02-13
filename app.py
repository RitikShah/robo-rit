from flask import Flask, request
from groupme.bot import Bot, url

app = Flask(__name__)
bot = Bot()

@app.route('/', methods=['POST'])
def webhook():
	bot.webhook(data=request.get_json())

@bot.command()
def test():
	print('lol cool')
	bot.send_message('Success!')

@bot.listener()
def test2(msg)
	print(msg)
	bot.send_message(f'HELP ME YUYU {msg}')