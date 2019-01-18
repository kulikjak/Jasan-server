import os
import flask

from server.app import app

api = flask.Blueprint('email', __name__)


@app.route('/inbox')
def inbox():
    return flask.render_template('inbox.html')


@api.route('', methods=['GET', 'POST'])
def email():
    if flask.request.method == 'GET':
        pass
    else:
        pass


@api.route('/<mail_id>/move/<folder_id>', methods=['GET'])
def email_move(mail_id, folder_id):
    mail = g.model.mails.find_one(mail_id)
    if mail is None:
        return jsonify({})

    metadata = mail.metadata
    metadata['folder'] = folder_id
    mail.metadata = metadata

    return jsonify(mail.get_serialized_data())


@api.route('/<mail_id>/toggle_read', methods=['GET'])
def email_toggle_read(mail_id):
    mail = g.model.mails.find_one(mail_id)
    if mail is None:
        return jsonify({})

    metadata = mail.metadata
    metadata['read'] = False if 'read' not in metadata else not metadata['read']
    mail.metadata = metadata

    return jsonify(mail.get_serialized_data())


@api.route('/admin', methods=['GET'])
def admin_mail():
    pass


app.register_blueprint(api, url_prefix='/email')
