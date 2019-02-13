from flask import Flask, request
from groupme.bot import Bot, url

app = Flask(__name__)
bot = Bot()

@app.route('/', methods=['POST'])
def webhook(self):
	bot.webhook(data=request.get_json())

@bot.command(name='test')
def test():
	send_message('Success!')