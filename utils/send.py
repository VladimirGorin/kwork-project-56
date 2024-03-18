

class Send:
    def __init__(self, logger) -> None:
        self.logger = logger

    def info_log(self, message):
        print(message)
        self.logger.info(message)

    def error_log(self, message):
        print(message)
        self.logger.error(message)

    def send_groups(self, groups, text):
        try:

            pass

        except Exception as e:
            self.error_log(f"Ошибка!: {e}")
