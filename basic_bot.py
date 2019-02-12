from groupme.bot import Bot, url

test = Bot()

@test.command(name=test)
def test():
	send_message('Success!')