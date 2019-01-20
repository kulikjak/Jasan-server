import os
import hashlib
import flask
import flask_login

from flask_login import login_required
from flask_login import UserMixin

from server.model import Model
from server.app import app

from flask_login import login_required

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return flask.g.model.users.find_one(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')

    elif flask.request.method == 'POST':

        # get credentials from POST request
        username = flask.request.form['username'].lower()
        password = flask.request.form['password']
        phash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        users = flask.g.model.users.find_query({'name': username})
        if not users:
            return flask.render_template('login.html')

        user = users[0]
        if user.password == phash:
            flask_login.login_user(user)

            return flask.redirect(flask.request.args.get('next') or flask.url_for('admin'))

        return flask.render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('home'))


@app.route('/admin')
@login_required
def admin():
    feedbacks = flask.g.model.feedbacks.find()
    return flask.render_template('admin.html', feedbacks=feedbacks)


@app.route('/')
def home():
    return flask.render_template('home.html')


#@app.route('/void', methods=['GET', 'POST'])
#def void():
#    return flask.render_template('void.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if flask.request.method == 'GET':
        return flask.render_template('feedback.html')

    elif flask.request.method == 'POST':
        data = {
            'title': flask.request.form['feedback_title'],
            'text': flask.request.form['feedback_text']
        }
        flask.g.model.feedbacks.create(data)
        flask.flash('Děkujeme za zpětnou vazbu', 'success')

        return flask.redirect(flask.url_for('feedback'))


@app.route('/journal', defaults={'path': ''})
@app.route('/journal/<path:path>')
def routing(path):
    # prepare path and remove trailing slashes
    path = 'journal/{}'.format(path).rstrip('/')

    # given path does not exists
    if not os.path.exists(path):
        return "This path does not exists: {}".format(path), 404

    # given path is directory
    if os.path.isdir(path):
        listing = os.listdir(path)
        _dirs = [d for d in listing if os.path.isdir(os.path.join(path, d))]
        _files = [f for f in listing if os.path.isfile(os.path.join(path, f))]
        _back = path.rsplit('/', 1)[0] if (path != app.config['JOURNAL_ROOT']) else None

        return flask.render_template(
            'filemanager.html',
            dirs=_dirs,
            files=_files,
            back=_back,
            path=path,
            server=app.config['SERVER_ADDRESS'])

    # given path is file
    if os.path.isfile(path):
        _dir, _file = path.rsplit('/', 1)
        return flask.send_from_directory(directory=_dir, filename=_file)

    return "Internal server error", 500


@app.route('/uploads/<image>')
def uploads(image):
    image = 'uploads/{}'.format(image)
    if os.path.isfile(image):
        _dir, _file = image.rsplit('/', 1)
        return flask.send_from_directory(directory=_dir, filename=_file)

    return "Nothing to show", 404
