# chess-bot

Inspired by [Lichess-bot](https://github.com/ShailChoksi/lichess-bot). Bot uses Stockfish chess engine software and Lichess API. Simple bridge between chess engine and Lichess API. Simply stream game moves, provides them to engine and make moves. More you can see [Lichess API](https://lichess.org/api)

## Instalation

First install all requirements located in `engine/data/requirements.txt` file. After that download [Stockfish chess engine](https://stockfishchess.org/download/) and all files put in `engine/stockfish` folder. Exe file needs to be named stockfish.exe.

## Usage

To use simply run `python main.py <TOKEN>` into CMD. To get token you need to make App in Lichess settings or you can use JS oauth server located in `src/oauth`, check below for instructions. Bot automatically would accept any challege and start playing with them. It is setup to be 500ms per turn, you can increase or decrease in `src/chess/engine.py` file. 

```
18  result = self.engine.play(board, chess.engine.Limit(time=0.5))
```

### Using oauth to get token

Locate to `src/oauth` and first run `npm install`. After install run `node server.js`, in browser type http://localhost:3000/login, click on Login and follow steps. After authorization you would be redirected to http://localhost:3000/callback with token, save it somewhere to not lose it.
