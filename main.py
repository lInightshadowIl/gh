import hashlib
import time
import random
import string
import requests as req

import os
numeros = os.environ.get('num')
token = os.environ.get('tok')
tuid = os.environ.get('tui')

salt = "6cqshh5dhw73bzxn20oexa9k516chk7s"  # borrowed from https://github.com/thesadru/genshinstats




def calculate_ds():  # borrowed from https://github.com/thesadru/genshinstats
  t = int(time.time())
  r = "".join(random.choices(string.ascii_letters, k=6))
  h = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()
  return f"{t},{r},{h}"


USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

headers = {
    # required headers
    "x-rpc-app_version": "1.5.0",
    "x-rpc-client_type": "4",
    "x-rpc-language": "en-us",
    # authentications headers
    "ds": calculate_ds(),
    # recommended headers
    "user-agent": USER_AGENT
}

resp = req.get(
    'https://bbs-api-os.hoyoverse.com/game_record/genshin/api/dailyNote',
    params=dict(server='os_usa', role_id=numeros, schedule_type=1),
    headers=headers,
    cookies={
        'ltuid_v2': tuid,
        'ltoken_v2': token
    })

print(resp.text)
