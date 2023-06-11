import logging
import traceback


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('digestor.log')
        self.logger.addHandler(file_handler)

    # Handles errors output
    # Print the error message to a logfile
    # but in production you should probably
    # want to log to a database instead
    def store(self):
        self.logger.warning(traceback.format_exc())
