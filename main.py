import hashlib
import time
import random
import string
import requests as req
import os
import json

numeros = os.environ.get('num')
token = os.environ.get('tok')
tuid = os.environ.get('tui')

salt = "6cqshh5dhw73bzxn20oexa9k516chk7s"


def calculate_ds():
  t = int(time.time())
  r = "".join(random.choices(string.ascii_letters, k=6))
  h = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()
  return f"{t},{r},{h}"


USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

headers = {
    "x-rpc-app_version": "1.5.0",
    "x-rpc-client_type": "4",
    "x-rpc-language": "en-us",
    "ds": calculate_ds(),
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

# Verifica si la solicitud fue exitosa (código de respuesta 200)
if resp.status_code == 200:
  # Parsea la respuesta JSON
  response_data = json.loads(resp.text)

  # Accede a las propiedades deseadas
  current_resin = response_data.get('data', {}).get('current_resin')
  max_resin = response_data.get('data', {}).get('max_resin')
  resin_recovery_time = response_data.get('data',
                                          {}).get('resin_recovery_time')
  current_home_coin = response_data.get('data', {}).get('current_home_coin')
  home_coin_recovery_time = response_data.get(
      'data', {}).get('home_coin_recovery_time')
  finished_task_num = response_data.get('data', {}).get('finished_task_num')
  total_task_num = response_data.get('data', {}).get('total_task_num')
  expeditions = response_data.get('data', {}).get('expeditions')

  # Imprime los valores
  print("current_resin:", current_resin)
  print("max_resin:", max_resin)
  print("resin_recovery_time:", resin_recovery_time)
  print("current_home_coin:", current_home_coin)
  print("home_coin_recovery_time:", home_coin_recovery_time)
  print("finished_task_num:", finished_task_num)
  print("total_task_num:", total_task_num)
  print("expeditions:", expeditions)
else:
  print("Error en la solicitud:", resp.status_code)
  print(resp.text)
