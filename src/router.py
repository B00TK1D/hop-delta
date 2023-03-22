import flask

import waittime

# Initialize flask
app = flask.Flask(__name__)

def run():
    global app
    # Run the app
    app.run(port=2023, host="0.0.0.0", debug=True, use_evalex=False)

### Routes ###
@app.route("/", methods=["GET"])
def route_exploits():
    return waittime.dashboard()

@app.route("/reset", methods=["GET"])
def route_reset():
    return waittime.reset()