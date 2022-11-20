import logging
import sys
import requests

class Logger:
    def __init__ (self, logger_name, log_level=None, url=""):
        self.url = url
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        sh = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(sh)
        self.logger.setLevel(logging.INFO)

    def error(self, message):
        self.logger.error(message)
        self.send_webhook("error", message)
    
    def warning(self, message):
        self.logger.warning(message)
        self.send_webhook("warning", message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)


    def send_webhook(self, title, message):
        assert self.url != "", "url is not set"
        self.data = {"username": self.logger_name}
        self.data["embeds"] = [{"title": title, "description": message}]
        result = requests.post(self.url, json=self.data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))
