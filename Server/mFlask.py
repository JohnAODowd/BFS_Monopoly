from flask import Flask, request, render_template
import redisLib as r
import lobby
from json import dumps
print("START *****************************************************************************************************")

app = Flask(__name__)

"""
Application Controller
"""

# TODO fill in web pages

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
            gID = lobby.getfirstPublicGame()                                    #get first available game
            if gID:
                return render_template("join.html", gID=gID)                    #return form
            else:
                return render_template("join.html", error="No games available")
        else:
            return render_template("error.html")                                #Else invalid parameters
    else:
        return render_template("error.html")                                    #error


"""
Main game controller
"""
@app.route("/game", methods=["POST"])                                           #Only use post here
def game():
    if request.method == "POST":
        json = (request.get_json())
        if 'gID' in json and 'uID' in json:                                     #if user has valid uID and gID
            if r.validategID(json['gID']) and r.validateUID(json['gID'], json['uID']):
                if json['request'] == 'FIGURINE':                               #user selecting figurine
                    ret = lobby.selectFigurine(json)
                elif json['request'] == 'PING' and lobby.getGameStatus(json['gID']) == "LOBBY":
                    ret = lobby.ping(json)
                    
        elif 'gID' in json:
            if r.validategID(json['gID']):                                      #set join user details
                if json['request'] == 'JOIN':
                    ret = lobby.join(json)
        else:
            if json['request'] == 'HOST':                                       #set host user details
                ret = lobby.host(json)


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