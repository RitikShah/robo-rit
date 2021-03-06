import os
import sys
import json
import functools

import requests

from flask import Flask, request
from decorator import decorator

from .exceptions import ConfigException, GroupMeException

url  = 'https://api.groupme.com/v3/bots/post'

class Bot:
	''' Class to define a single groupme bot '''

	def __init__(self, prefix='.'):
		try: self._id = os.getenv('GROUPME_BOT_ID')
		except Exception:
			raise ConfigException('Missing Bot ID. Run Heroku Config: Set GROUPME_BOT_ID=[bot-id-here]')

		try: self._name = os.getenv('GROUPME_BOT_NAME')
		except Exception:
			raise ConfigException('Missing Bot Name. Run Heroku Config: Set GROUPME_BOT_NAME=[bot-name-here]')

		self._listeners = dict()
		self._commands = dict()

		self._prefix = prefix

		self.send_message('Successfully Booted!')

	def webhook(self, data):
		''' Receives the raw json from each message (POST from groupme callback URL) '''
		
		# Ignore message if sent by bot
		if self.isBot(data['name']):
			self.log(f'Received {self._name} message')

			return "ok", 200

		self.log(f'Received {data}')

		success = self.received(data)
		if success == -1:
			self.invalid_command(data)
		else:
			self.log(f'Successfully executed {success}')

		return "ok", 200

	def received(self, data):
		''' Forward message to listeners and commands '''
		
		if data['text'][0] != prefix: # only to listeners if not a bot command
			for listener in self._listeners:
				listener(data)
		else:
			msg = data['text'][1:] # exclude prefix
			words = msg.split(' ')

			for command in self._commands:
				if command.getattr(_command_name) == words[0]:
					command(words[1:])
					return command.getattr(_command_name)

			# No command found
			return -1

	@decorator
	def listener(self, func, *args, **kwargs):
		""" Decorator for functions to listen to each message """
		
		self._listeners[func.__name__] = func
		return func(*args, **kwargs)

	# Adapted from https://github.com/angrox/groupme-bot/blob/master/groupmebot.py	
	@decorator
	def command(self, func, hidden=False, name=None, *args, **kwargs):
		""" Decorator for bot command functions. Only runs functions when command is called """
		
		setattr(func, '_command', True)
		setattr(func, '_hidden', hidden)
		setattr(func, '_command_name', name or func.__name__)

		self._commands[name or func.__name__] = func
		return func(*args, **kwargs)

	def send_message(self, msg):
		''' Sends a message to the groupchat through POST '''

		data = {
			'bot_id' : self._id,
			'text'   : msg
		}
		
		self.log(f'Sending: {data} at {url}')
		requests.post(url, data)

	def invalid_command(self, data):
		''' Sends a message notifying the user of an invalid command '''

		cmd = msg.split(' ')[0]
		self.send_message(f'{cmd} is an invalid command.')

	def isBot(self, author):
		return author == self._name

	# Todo: use logging module
	def log(self, msg):
		print(f'{self._name}: {str(msg)}')
		sys.stdout.flush()