import install

from utils.send import Send

import logging, sys


class Main():

    def __init__(self):
        self.logger = self.initialize_logger()
        self.start()

    def start(self):
        try:
            groups = self.read_file("./assets/data/groups.txt", "lines")
            groups = [line.strip() for line in groups]

            text = self.read_file("./assets/data/text.txt")

            send = Send(self.logger)
            send.send_groups(groups, text)

        except Exception as e:
            self.error_log(f"Ошибка!: {e}")

    def error_log(self, message):
        print(message)

        self.logger.error(message)
        input("\nНажмите ENTER что бы закрыть консоль.")
        sys.exit(1)

    def read_file(self, path, read_format="normal"):
        with open(path, 'r', encoding="utf-8") as file:
            if read_format == "normal":
                data = file.read()
            elif read_format == "lines":
                data = file.readlines()

        return data

    def initialize_logger(self):
        logger = logging.getLogger("GLOBAL")
        logger.setLevel(logging.DEBUG)

        log_file = './assets/logs/main.log'
        file_handler = logging.FileHandler(filename=log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger


try:
    if __name__ == "__main__":
        Main()
        input("\nНажмите ENTER что бы закрыть консоль.")

except KeyboardInterrupt:
    sys.exit(1)
