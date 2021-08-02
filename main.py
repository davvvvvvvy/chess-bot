from src.api.lichess import Lichess
from src.chess.engine import ChessEngine
from src.db.db import DB
from datetime import datetime

import time
import sys
token = sys.argv[1]

engine = ChessEngine()
lichess = Lichess(token)

def game():
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
				print(f'[{datetime.now().strftime("%H:%M:%S")}]: Game started!')
				checker=True
				while checker:
					gameId, fen, isMyTurn, color = lichess.streamGame()
					move = engine.getMove(fen, color)
					lichess.makeMove(gameId, isMyTurn, move)
					if stream['type'] == "gameFinish":
						checker=False
		except:
			pass

def seek():
	while True:
		try:
			lichess.createSeek()
			time.sleep(60*7.5)
		except Exception as e:
			print(e)

import threading

threading.Thread(target=game).start()
threading.Thread(target=seek).start()