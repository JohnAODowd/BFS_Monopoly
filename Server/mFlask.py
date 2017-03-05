from json import dumps
from flask import Flask, request, render_template
from monopoly import lobby, gameLib, helpers, getData

print("START *****************************************************************************************************")

app = Flask(__name__)

"""
Application Controller
"""

@app.route('/', methods=["GET"])
def home():
    if request.method == "GET":
        if request.args.get("gID"): 
            gID = request.args.get("gID")
            return render_template("index.html", joinForm="private", gID=gID)
    return render_template("index.html", joinForm="public")                             #return the homepage

# TODO check for form to implement full server independence
"""
Main game controller
"""
@app.route("/game", methods=["POST", "GET"])
def game():
    ret = "{'error':'broken'}"
    if request.method == "POST":
        json        = (request.get_json())
        fromForm    = False
        if json == None:
            print(json)
            fromForm = True
            form = request.form
            json = helpers.formToJson(form)

        if json['request'] == 'HOST' or json['request'] == "JOIN" or helpers.getGameState(json['gID']) == "LOBBY":
            ret = lobby.lobby(json)
            if fromForm:
                if json['request'] == "HOST" or json['request'] == "JOIN":
                    if 'error' in ret:
                        return render_template("index.html", error=ret['error'])
                    else:
                        return render_template("game.html", initFigurines=str(dumps(getData.getFigurinesJson())), init=str(dumps(ret)))

        elif helpers.getGameState(json['gID']) == "PLAYING":
             ret = gameLib.game(json)
        elif helpers.getGameState(json['gID']) == "AUCTION":
             ret = gameLib.bid(json)

        return dumps(ret)

if __name__ == '__main__':
  app.run(
        host="0.0.0.0",
        port=int("8080")
  )