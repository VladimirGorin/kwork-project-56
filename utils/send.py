from telethon.sync import TelegramClient, errors, functions

from configparser import ConfigParser

import time

config = ConfigParser()
config.read("./assets/data/config.ini")

class Send:
    def __init__(self, logger) -> None:
        self.logger = logger

        self.stats = {
            "groups_sended_count": 0

        }

    def info_log(self, message):
        print(message)
        self.logger.info(message)

    def error_log(self, message):
        print(message)
        self.logger.error(message)

    def auth(self):
        try:

            phone_number = config.get("SETTINGS", "PHONE")
            api_id = int(config.get("SETTINGS", "API_ID"))
            api_hash = config.get("SETTINGS", "API_HASH")


            session_path = f"./assets/sessions/{phone_number}.session"
            success_message = "Вы успешно авторизовались под своим аккаунтом"

            self.client = TelegramClient(session_path, api_id, api_hash)
            self.client.connect()

            if not self.client.is_user_authorized():
                self.client.start(phone=phone_number)

            self.info_log(success_message)

        except Exception as e:
            self.error_log(f"Ошибка!: {e}")

    def flood_wait(self, error):
        seconds = error.seconds
        self.info_log(f"Попали в лимит спим {seconds} секунд : {error}")
        time.sleep(seconds)

    def send_groups(self, groups, text, image_path):
        try:

            for group in groups:
                try:
                    self.client(functions.channels.JoinChannelRequest(group))
                    self.info_log(f"Вступили в группу: {group}")
                    time.sleep(2)
                    self.client.send_message(group, text)
                    self.client.send_file(group, image_path, caption=text)
                    self.stats = self.stats["groups_sended_count"] + 1
                    time.sleep(2)

                except (errors.FloodError) as e:
                    self.flood_wait(e)
                    continue

                except Exception as e:
                    self.error_log(
                        f"[{group}] Ошибка при работе с группой, продолжаем: {e}")

            self.info_log(f"Рассылка завершена\nВсего отправлено сообщений: {self.stats['groups_sended_count']}")
            self.client.disconnect()

        except Exception as e:
            self.error_log(f"Ошибка!: {e}")
