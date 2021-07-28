import chess, chess.engine, chess.svg
from datetime import datetime

class ChessEngine():
	engine = None
	
	def __init__(self):
		self.engine = chess.engine.SimpleEngine.popen_uci('engine/stockfish/stockfish.exe')
		print(f'[{datetime.now().strftime("%H:%M:%S")}]: Engine started!')

	def getMove(self, fen, color):
		try:
			board = chess.Board(fen)
			if color == 'black':
				board.turn = chess.BLACK
			if color == 'white':
				board.turn = chess.WHITE
			result = self.engine.play(board, chess.engine.Limit(time=0.5))
			return result.move
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: {e}')
			self.engine = chess.engine.SimpleEngine.popen_uci('engine/stockfish/stockfish.exe')

	def checkForCheckmate(self, fen):
		board = chess.Board(fen)
		return board.is_game_over()

	def stop_engine(self):
		self.engine.quit()