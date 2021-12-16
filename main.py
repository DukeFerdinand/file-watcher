import json
from time import sleep
from pymongo import MongoClient


class FileLooper:
    song_txt: str
    mongo: MongoClient
    last_song: str
    current_song: str

    def __init__(self, c: dict):
        self.song_txt = c["song_file"]
        self.last_song = ""
        self.current_song = ""

        self.mongo = MongoClient(c["db_string"])
        self.db = self.mongo.get_default_database()
        self.collection = self.db.get_collection('current_song')

    def check_and_log(self):
        try:
            print("[loop] Polling song TXT file...")
            file = open(self.song_txt)
            current_song = file.readline()
            if self.current_song != current_song:
                print("[loop] Got a new song!")
                self.last_song = self.current_song
                self.current_song = current_song

                # last = self.last_song.split('-')
                self.collection.find_one_and_replace(filter={"type": "last_song"},
                                                     replacement={
                                                         "type": "last_song",
                                                         "song_string": self.last_song,
                                                     },
                                                     upsert=True
                                                     )
                self.collection.find_one_and_replace(filter={"type": "current_song"},
                                                     replacement={
                                                         "type": "current_song",
                                                         "song_string": self.current_song,
                                                     },
                                                     upsert=True
                                                     )
        except FileNotFoundError:
            print("Could not find the song TXT file!")

    def run_loop(self):
        while True:
            self.check_and_log()
            sleep(5)


def watcher_loop(conf: dict):
    """The 'meat' of the app. This will run as long as the """
    print("[loop] Starting watcher loop...")
    looper = FileLooper(conf)
    looper.run_loop()


# This is a sample Python script.
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('[proc] Running Botsuro song watcher...')
    try:
        print("[proc] Checking for proper config...")
        f = open("config.json").read()
        config = json.loads(f)
        watcher_loop(config)
    except FileNotFoundError:
        print("Cannot find config.json! Please add it next to this .exe file.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
