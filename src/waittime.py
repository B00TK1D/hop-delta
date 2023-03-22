import flask

import db
import scanner

def dashboard():

    # Get the wait time
    t = db.get_wait_time()

    #if (t > 60):
    if False:
        t = t / 60
        t = str(int(t)) + " minutes"
    else:
        t = str(int(t)) + " seconds"

    f = db.get_factors()

    return flask.render_template("waittime.html", time=t, factors=f)


def reset():
    scanner.reset()

    return flask.redirect("/")
