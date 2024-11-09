import re
from datetime import datetime
import json

from haralyzer import HarParser


class Message:
    def __init__(self, text, author, date):
        self.text = text
        self.author = author
        self.date = datetime.fromisoformat(date)

    def export(self):
        return "{0} @ {1}: \n {2} \n".format(self.author, self.date.strftime("%m/%d/%y %I:%M"), self.text)

    def export_dict(self):
        return {"author": self.author, "date": self.date.strftime("%m/%d/%y %I:%M"), "text": self.text}


def har_to_arr(name_of_file):
    archive = HarParser.from_file(name_of_file)
    instance_archive = []
    for page in archive.pages:
        for entry in page.entries:
            if entry.request.method == "GET" and re.search("https:\/\/discord.com\/api\/.*\/messages.*", entry.request.url):
                try:
                    msgs = json.loads(entry.response.text)
                    for msg in msgs:
                        instance_archive.append(Message(msg["content"], msg["author"]["username"], msg["timestamp"]))
                except:
                    pass

    instance_archive.sort(key=lambda x: x.date)
    return instance_archive


# Write the results of array_msg to the files with optional prefix based on metadata
def file_writer(array_msg, plain_bool, json_bool, meta=""):
    if plain_bool:
        plainText = open(((meta + "_") if meta else "") + "PlainTextMessages.txt", "w", encoding="utf-8")
        for msg in array_msg:
            plainText.write(msg.export())
        plainText.close()

    if json_bool:
        jsonText = open(((meta + "_") if meta else "") + "JSONMessages.json", "w", encoding="utf-8")
        json.dump(array_msg, jsonText, default=lambda a: a.export_dict())
        jsonText.close()
    return
