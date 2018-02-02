import sys
import time
import logging

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


def check_config(app):
    print('Checking configuration file: ', end='')

    if not app.config['SERVER_ADDRESS'].startswith('http://'):
        print('\nSERVER_ADDRESS variable must start with http://')
        sys.exit()

    if not app.config['SERVER_ADDRESS'].endswith('/'):
        print('\nSERVER_ADDRESS variable must end with /')
        sys.exit()

    if len(app.config['SERVER_ADDRESS']) < 8:
        print('\nSERVER_ADDRESS variable must contain some real address...')
        sys.exit()

    print('OK')