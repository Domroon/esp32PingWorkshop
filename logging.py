CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10

class Logger:
    def __init__(self, log_level=INFO):
        self.log_level = log_level

    def critical(self, msg):
        if self.log_level <= CRITICAL:
            print("[CRITICAL]", msg)

    def error(self, msg):
        if self.log_level <= ERROR:
            print("[ERROR]", msg)

    def warning(self, msg):
        if self.log_level <= WARNING:
            print("[WARNING]", msg)

    def info(self, msg):
        if self.log_level <= INFO:
            print("[INFO]", msg)

    def debug(self, msg):
        if self.log_level <= DEBUG:
            print("[DEBUG]", msg)
