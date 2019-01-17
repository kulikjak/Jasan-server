import logging
import os
import urllib

import flask
import flask_login
import pymongo

from flask_login import login_required
from flask_login import UserMixin

from server.model import Model
from server.util import check_config
from server.util import setup_logging

from server.util import generate_random_filename
from server.util import create_thumbnail

# create logger
logger = logging.getLogger(__name__)
setup_logging()

# create Flask application
app = flask.Flask(__name__)
app.config.from_pyfile('config.py')

check_config(app)

# prepare database connection
parsed = urllib.parse.urlsplit(app.config['MONGODB_URI'])
mongo_client = pymongo.MongoClient(app.config['MONGODB_URI'])
db = mongo_client[parsed.path[1:]]

# init model for Zpevnik application
model = Model(db=db)


@app.before_request
def before_request():
    flask.g.model = model


# User base class
class User(UserMixin):

    def __init__(self):
        self.id = 0


login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User()


def allowed_upload_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ----- routing ----- #


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/void', methods=['GET', 'POST'])
def void():
    return flask.render_template('void.html')


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


@app.route('/screambook', methods=['GET', 'POST'])
def screambook():
    user_id = flask.request.cookies.get('jasanUIDCookie')

    if flask.request.method == 'GET':
        screams = flask.g.model.screams.find()
        return flask.render_template('social.html', screams=screams, user_id=user_id)

    elif flask.request.method == 'POST':
        filename = None

        scream_name = flask.request.form['scream_name']
        scream_text = flask.request.form['scream_text']

        if scream_name is None or scream_name == '':
            flask.flash('Výkřik musí mít zadané jméno', 'danger')
            return flask.redirect(flask.url_for('screambook'))

        if scream_text is None or scream_text == '':
            flask.flash('Výkřik musí mít nějaký text', 'danger')
            return flask.redirect(flask.url_for('screambook'))

        # check for file upload
        if 'scream_attachment' in flask.request.files:
            file = flask.request.files['scream_attachment']

            if file and allowed_upload_file(file.filename):
                extension = file.filename.rsplit('.', 1)[1].lower()
                filename = '{}.{}'.format(generate_random_filename(), extension)
                complete_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(complete_path)
                create_thumbnail(complete_path, 128)

        data = {
            'name': scream_name,
            'text': scream_text,
            'user_id': flask.request.cookies.get('jasanUIDCookie'),
            'attachment': filename
        }
        flask.g.model.screams.create(data)
        flask.flash('Výkřik uložen', 'success')
        return flask.redirect(flask.url_for('screambook'))


@app.route('/screambook/delete/<scream_id>', methods=['GET'])
def screambook_delete(scream_id):
    user_id = flask.request.cookies.get('jasanUIDCookie')

    # check if this scream belongs to current user
    scream = flask.g.model.screams.find_one(scream_id)
    if scream.user_id != user_id or user_id == None:
        flask.flash('Tento výkřik není tvůj!', 'danger')
        return flask.redirect(flask.url_for('screambook'))

    flask.g.model.screams.delete(scream)
    flask.flash('Výkřik vymazán', 'success')

    return flask.redirect(flask.url_for('screambook'))


@app.route('/screambook/<scream_id>/like')
def screambook_like(scream_id):
    scream = flask.g.model.screams.find_one(scream_id)

    scream.popularity += 1
    flask.g.model.screams.save(scream)
    return flask.redirect(flask.url_for('screambook'))


@app.route('/screambook/<scream_id>/dislike')
def screambook_dislike(scream_id):
    scream = flask.g.model.screams.find_one(scream_id)

    scream.popularity -= 1
    flask.g.model.screams.save(scream)
    return flask.redirect(flask.url_for('screambook'))


@app.route('/skautis')
def skautis():
    return flask.Response("Hello SkautIS!")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')

    elif flask.request.method == 'POST':

        # get credentials from POST request
        password = flask.request.form['password']

        # check user credentials
        if password == app.config['ADMIN_PASSWORD']:
            flask_login.login_user(User())
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


@app.route('/uploads/<image>')
def uploads(image):
    image = 'uploads/{}'.format(image)
    if os.path.isfile(image):
        _dir, _file = image.rsplit('/', 1)
        return flask.send_from_directory(directory=_dir, filename=_file)

    return "Nothing to show", 404


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