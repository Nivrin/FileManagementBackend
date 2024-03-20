import logging
import os

from logging.handlers import RotatingFileHandler


def setup_logging():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    logs_dir = os.path.join(current_dir, '..', '..', 'logs')

    log_file = os.path.join(logs_dir, 'app.log')

    os.makedirs(logs_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
        ]
    )

    logger = logging.getLogger('my_app')
    logger.setLevel(logging.INFO)

    return logger
