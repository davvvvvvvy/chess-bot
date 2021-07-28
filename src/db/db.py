from os import write
import sqlite3
from datetime import datetime

""" type, challengeId, challener
challenge, 82ZNwWdy, username """

class DB():
	con = sqlite3.connect('engine/data/database.db')
	cur = con.cursor()
	_type = None
	challengeId = None
	challenger = None
	
	def __init__(self, _type, challengeId, challenger):
		self._type = _type
		self.challengeId = challengeId
		self.challenger = challenger

	def createTable(self):
		try:
			self.cur.execute('CREATE TABLE challenge (type text, challengeId text, challenger type)')
			self.con.commit()
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: Table exists')

	def insertInto(self):
		try:
			self.cur.execute(f'INSERT INTO challenge VALUES ("{self._type}", "{self.challengeId}", "{self.challenger}")')
			self.con.commit()
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: {e}')
	
	def selectAll(self):
		csv = open('engine/data/data.csv')
		csv.write('type,challengeId,challenger\n')
		try:
			for select in self.cur.execute('SELECT * FROM challenge'):
				csv.write(f'{select[0]},{select[1]},{select[2]}\n')
			csv.close()
		except Exception as e:
			print(f'[{datetime.now().strftime("%H:%M:%S")}]: {e}')

	def closeConnection(self):
		self.con.close()