from json import dumps
import monopoly.redisLib as r
import monopoly.monopolyVars as mv
from flask import Flask, request, render_template
from monopoly import lobby, gameLib, helpers

print("START *****************************************************************************************************")

app = Flask(__name__)

"""
Application Controller
"""

# TODO fill in web pages
# TODO separate game() into functions

@app.route('/', methods=["GET"])
def home():
    if request.method == "GET":
        if request.args.get("gID"): 
            gID = request.args.get("gID")
            return render_template("index.html", joinForm="private", gID=gID)
    return render_template("index.html", joinForm="public")                             #return the homepage


"""
Main game controller
"""
@app.route("/game", methods=["POST", "GET"])                                           #Only use post here
def game():
    ret = "{'error':'broken'}"
    if request.method == "POST":
        json = (request.get_json())

        if json == None:
            form = request.form
            json = helpers.formToJson(form)
        if json['request'] == 'HOST' or json['request'] == "JOIN" or lobby.getGameStatus(json['gID']) == "LOBBY":
            ret = lobby.lobby(json)
            print(ret)
        if json['request'] == "HOST" or json['request'] == "JOIN":
            if 'error' in ret:
                return render_template("index.html", error=ret['error'])
            else:
                return render_template("game.html", initFigurines=str(dumps(mv.getFigurines(True))), init=str(dumps(ret)))
        # elif lobby.getGameStatus(json['gID']) == "PLAYING":
        #     ret = gameLib.game(json)
        # elif lobby.getGameStatus(json['gID']) == "AUCTION":
        #     ret = gameLib.bid(json)

        return dumps(ret)

        # TODO Lobby:
            # TODO keep track of lobby time per ping
            # TODO init Board
            # TODO set game

if __name__ == '__main__':
  app.run(
        host="0.0.0.0",
        port=int("8080")
  )