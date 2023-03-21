import flask

import db

def dashboard():

    # Get the wait time
    t = db.get_wait_time()

    if (t > 60):
        t = t / 60
        t = str(t) + " minutes"
    else:
        t = str(t) + " seconds"

    return flask.render_template("waittime.html", time=t)