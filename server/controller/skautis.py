import flask

from server.app import app

@app.route('/skautis')
def skautis():
    return flask.Response("Hello SkautIS!")
