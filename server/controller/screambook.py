import os
import flask

from server.app import app

from server.util import generate_random_filename
from server.util import create_thumbnail

api = flask.Blueprint('screambook', __name__)


@api.route('', methods=['GET', 'POST'])
def screambook():

    def allowed_upload_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
            return flask.redirect(flask.url_for('screambook.screambook'))

        if scream_text is None or scream_text == '':
            flask.flash('Výkřik musí mít nějaký text', 'danger')
            return flask.redirect(flask.url_for('screambook.screambook'))

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
        return flask.redirect(flask.url_for('screambook.screambook'))


@api.route('/delete/<scream_id>', methods=['GET'])
def screambook_delete(scream_id):
    user_id = flask.request.cookies.get('jasanUIDCookie')

    # check if this scream belongs to current user
    scream = flask.g.model.screams.find_one(scream_id)
    print(scream)
    if scream.user_id != user_id or user_id == None:
        flask.flash('Tento výkřik není tvůj!', 'danger')
        return flask.redirect(flask.url_for('screambook'))

    flask.g.model.screams.delete(scream)
    flask.flash('Výkřik vymazán', 'success')

    return flask.redirect(flask.url_for('screambook.screambook'))


@api.route('/<scream_id>/like')
def screambook_like(scream_id):
    scream = flask.g.model.screams.find_one(scream_id)

    scream.popularity += 1
    flask.g.model.screams.save(scream)
    return flask.redirect(flask.url_for('screambook.screambook'))


@api.route('/<scream_id>/dislike')
def screambook_dislike(scream_id):
    scream = flask.g.model.screams.find_one(scream_id)

    scream.popularity -= 1
    flask.g.model.screams.save(scream)
    return flask.redirect(flask.url_for('screambook.screambook'))


app.register_blueprint(api, url_prefix='/screambook')
