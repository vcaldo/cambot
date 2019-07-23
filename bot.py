#!/usr/bin/python3
import os
import time
import telebot
from watchdog.events import RegexMatchingEventHandler

class TelegramHandler(RegexMatchingEventHandler):
    IMAGES_REGEX = [r".*\.jpg$", r".*\.avi$"]
    #VIDEO_REGEX = [r".*\.avi$"]

    def __init__(self):
        super().__init__(self.IMAGES_REGEX)

    def check_open(self, event):
        print(str(event.src_path))
        for p in os.listdir("/proc/"):
            if not p.isdigit(): continue
            d = "/proc/%s/fd/" % p
            try:
                for fd in os.listdir(d):
                    f = os.readlink(d+fd)
                    if str(event.src_path) in f:
                        print("aberto")
                        return True
            except OSError:
                pass
        print("arquivo fechado")
        return False

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        fileopenstat = self.check_open(event)
        while fileopenstat:
            print("arquivo aberto checando de novo")
            fileopenstat = self.check_open(event)
        else:
                token = ""
                bot = telebot.TeleBot(token)
                if ".jpg" in event.src_path:
                    print("enviando msg")
                    chat_id=""
                    photo = open(event.src_path, 'rb')
                    bot.send_photo(chat_id, photo)
                    os.remove(event.src_path)
                elif ".avi" in event.src_path:
                    print("enviando video")
                    chat_id=""
                    video = open(event.src_path, 'rb')
                    bot.send_video(chat_id, video)
                    os.remove(event.src_path)
