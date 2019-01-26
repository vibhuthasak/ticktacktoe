from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = None
    return render_template("game.html", game=session["board"], turn=session["turn"], winner= session["winner"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    if(isOver(session["board"])):
      session["winner"] = session["turn"]

    if (session["turn"] == "X"):
      session["turn"] = "0"
    else:
      session["turn"] = "X"

    return redirect(url_for("index"))

@app.route("/newgame")
def newgame():
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    session["winner"] = None
    return redirect(url_for("index"))

def isOver(board):
  # Row win
  for row in board:
    if row[0] is not None and (row[0] == row[1] == row[2]):
      return True
    
  # Col win
  for col in range(3):
    if board[0][col] is not None and (board[0][col] == board[1][col] == board[2][col]):
      return True

  # Cross win
  if(board[0][0] is not None and (board[0][0] == board[1][1] == board[2][2])):
    return True
  
  if(board[0][2] is not None and (board[0][2] == board[1][1] == board[2][0])):
    return True

  return False