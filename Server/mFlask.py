from flask import Flask, request, render_template
import redisLib as r

print("START *****************************************************************************************************")

app = Flask(__name__)

def getfirstPublicGame():
    games   = r.getGames()
    for gID in games:
        if games[gID]["type"] == "public" and game[gID]["playersNo"] < 8:
            return gID
    return False

@app.route('/')
def home():
    return render_template("home.html")         #return the homepage

@app.route('/host')
def host():
    return render_template("host.html")         #return host form


@app.route("/join", methods=["GET"])
def join():
    if request.method == "GET":
        if request.args.get("gID"):                                             #check if private game
            gID     = request.args.get("gID")
            games   = r.getGames()
            if gID in games:                                                    #verify gID
                if games[gID]["PlayersNo"] == 8:                                #if game is full
                    return render_template("join.html", error="game full")
                else:
                    return render_template("join.html", gID=gID)                #return join form
        elif request.args.get("type") == "public":                              #check if game is join is public
            gID = getfirstPublicGame()                                          #get first available game
            if gID:
                return render_template("join.html", gID=gID)                    #return form
            else:
                return render_template("join.html", error="No games available")
        else:
            return render_template("error.html")                                #Else invalid parameters
    else:
        return render_template("error.html")                                    #error


@app.route("/game", methods=["POST"])                                           #Only use post here
def game():
    if request.method == "POST":
        pass
        # TODO set players
        # TODO Lobby:
            # TODO keep track of lobby time per ping
            # TODO init Board
            # TODO set game


def lobby(json):
    pass

if __name__ == '__main__':
  app.run(
        host="0.0.0.0",
        port=int("8080")
  )


