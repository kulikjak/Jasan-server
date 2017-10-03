import os
import time
import logging

from flask import Flask
from flask import redirect
from flask import render_template
from flask import send_from_directory

from colorlog import ColoredFormatter


def setup_handler(handler, level, fmt, use_colors=False):
    handler.setLevel(level)
    if use_colors:
        handler.setFormatter(
            ColoredFormatter(
                "%(log_color)s" + fmt,
                datefmt=None,
                reset=True,
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red',
                }))
    else:
        handler.setFormatter(logging.Formatter(fmt))
    return handler


def setup_logging():
    logging.Formatter.converter = time.gmtime

    rootLogger = logging.getLogger('')
    rootLogger.setLevel(logging.DEBUG)

    consoleFormat = ('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    consoleHandler = setup_handler(
        logging.StreamHandler(), logging.INFO, consoleFormat, use_colors=True)
    rootLogger.addHandler(consoleHandler)


# create logger
logger = logging.getLogger(__name__)
setup_logging()

# create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def main():
    return redirect(app.config['FILE_ROOT'])


@app.route('/<path:path>')
def routing(path):
    # remove trailing slashes
    path = path.rstrip('/')

    # given path does not exists
    if not os.path.exists(path):
        return "This path does not exists: {}".format(path), 404

    # check for simple path traversal attack
    if not app.config['FILE_ROOT'] in path:
        return "You are browsing wrong directory: {}".format(path), 404

    # given path is directory
    if os.path.isdir(path):
        listing = os.listdir(path)
        _dirs = [d for d in listing if os.path.isdir(os.path.join(path, d))]
        _files = [f for f in listing if os.path.isfile(os.path.join(path, f))]
        _back = path.rsplit('/', 1)[0] if (path != app.config['FILE_ROOT']) else None

        return render_template(
            'filemanager.html',
            dirs=_dirs,
            files=_files,
            back=_back,
            path=path,
            server=app.config['SERVER_ADDRESS'])

    # given path is file
    if os.path.isfile(path):
        _dir, _file = path.rsplit('/', 1)
        return send_from_directory(directory=_dir, filename=_file)

    return "Internal server error", 500


if __name__ == "__main__":
    logger.info('Listening on http://0.0.0.0:%d', app.config['SERVER_PORT'])
    app.run(host='0.0.0.0', port=app.config['SERVER_PORT'])
