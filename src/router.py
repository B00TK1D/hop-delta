import flask

import waittime

# Initialize flask
app = flask.Flask(__name__)

def run():
    global app
    # Run the app
    app.run(port=2000, host="0.0.0.0", debug=True, use_evalex=False, exclude_patterns=["/app/exploits/*"])

### Routes ###
@app.route("/", methods=["GET"])
def route_exploits():
    return waittime.dashboard()