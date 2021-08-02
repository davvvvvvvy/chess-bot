import json, requests
from datetime import datetime

class Lichess():
	api_key = None
	headers = None
	baseUrl = 'https://lichess.org'

	def __init__(self, api_key):
		self.api_key = api_key
		self.headers = {
			'Authorization': f'Bearer {self.api_key}',
			'Content-type': 'application/json'
		}
	
	###### Works on real-time and correspondence games ######
	def streamGame(self):
		try:
			url = 'https://lichess.org/api/account/playing'
			data = json.loads(requests.get(url, headers=self.headers).text)
			return str(data['nowPlaying'][0]['gameId']), str(data['nowPlaying'][0]['fen']), data['nowPlaying'][0]['isMyTurn'], str(data['nowPlaying'][0]['color'])
		except Exception as e:
			#print(f'[{datetime.now().strftime("%H:%M:%S")}]: {e}')
			pass

	###### Works on any game ######
	def streamAnyGame(self, gameId):
		try:
			url = f'https://lichess.org/api/stream/game/{gameId}'
			res = requests.get(url, headers=self.headers)
			return str(json.loads(res.text))
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: Error stream {e}')

	def makeMove(self, gameId, isMyTurn, move):
		try:
			if isMyTurn == True:
				url = f'https://lichess.org/api/board/game/{gameId}/move/{move}'
				data = json.loads(requests.post(url, headers=self.headers).text)
				return str(data)
			return
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: Error move {e}')

	def getEventStream(self):
		url = 'https://lichess.org/api/stream/event'
		return requests.get(url, headers=self.headers, stream=True)

	def isGameOver(self):
		try:
			response = self.getEventStream()
			lines = response.iter_lines()
			for line in lines:
				if line:
					if 'gameFinish' in json.loads(line.decode('utf-8')['type']):
						return json.loads(line.decode('utf-8'))
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: Error stream watch {e}')

	def watchStream(self):
		try:
			response = self.getEventStream()
			lines = response.iter_lines()
			for line in lines:
				if line:
					return json.loads(line.decode('utf-8'))
				else:
					return {'type': 'ping'}
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: Error stream watch {e}')

	def acceptChallenge(self, challengeId):
		try:
			url = f'https://lichess.org/api/challenge/{challengeId}/accept'
			return requests.post(url, headers=self.headers)
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: Error challange accept {e}')

	def createSeek(self):
		try:
			url = 'https://lichess.org/api/board/seek'
			return requests.post(url, headers={'Authorization': f'Bearer {self.api_key}'}, stream=True)
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: Error seek {e}')

	def streamGameState(self, gameId):
		url = f'https://lichess.org/api/board/game/stream/{gameId}'
		return requests.get(url, headers=self.headers, stream=True)
	
	def streamState(self, gameId):
		try:
			response = self.streamGameState(gameId)
			lines = response.iter_lines()
			for line in lines:
				if line:
					return json.loads(line.decode('utf-8'))
				else:
					return {'type': 'ping'}
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: {e}')