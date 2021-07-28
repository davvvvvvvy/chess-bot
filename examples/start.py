from src.api.lichess import Lichess
from src.chess.engine import ChessEngine
from datetime import datetime

import os
token = 'y2x0cURmgWt0yqXQ'

lichess = Lichess(token)

while True:
	try:
		stream = lichess.watchStream()
		print(stream)
		if stream['type'] == 'challenge':
			challengeId = lichess.acceptChallenge(stream['challenge']['id'])
			if challengeId.status_code == 200:
				print(f'[{datetime.now().strftime("%H:%M:%S")}]: Challenge accepted!')
			else:
				print(challengeId)
		if stream['type'] == 'gameStart':
			os.system(f'python main.py {token}')
		if stream['type'] == 'gameFinish':
			print(stream)
	except:
		pass