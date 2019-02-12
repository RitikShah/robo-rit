from groupme.bot import Bot, url, app

test = Bot()

@test.command(name=test)
def test():
	send_message('Success!')