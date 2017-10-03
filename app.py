import time
import logging

from flask import Flask
from flask import redirect
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
	return redirect("/root")

@app.route('/<path:path>')
def routing(path):
    return 'You want path: %s' % path



if __name__ == "__main__":
    logger.info('Listening on http://0.0.0.0:%d', app.config['SERVER_PORT'])
    app.run(host='0.0.0.0', port=app.config['SERVER_PORT'])
