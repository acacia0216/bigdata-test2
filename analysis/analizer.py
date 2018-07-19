import json
import re
from collections import Counter

from konlpy.tag import Twitter


def json_to_str(filename, key):
    jsonfile = open(filename, "r", encoding="utf-8")
    json_string = jsonfile.read()
    jsondata = json.loads(json_string)

    # print(type(json_string))
    # print(json_string)

    data = ""

    for item in jsondata:
        value = item.get(key)
        if value is None:
            continue

        data += re.sub(r'[^\w]', '', value)

    return data


def count_wordfreq(data):
    twitter = Twitter()
    twitter.nouns(data)
    nouns = twitter.nouns(data)
    print(nouns)

    count = Counter(nouns)
    return count

# dataString = json_to_str(filename, "message_str")
# print(dataString)
