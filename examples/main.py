from src.api.lichess import Lichess
from src.chess.engine import ChessEngine
from datetime import datetime

import sys
token = sys.argv[1]

engine = ChessEngine()
lichess = Lichess(token)

while True:
	gameId, fen, isMyTurn, color = lichess.streamGame()
	move = engine.getMove(fen, color)
	lichess.makeMove(gameId, isMyTurn, move)