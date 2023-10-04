# -*- coding: utf-8 -*-

from utils import main, get_previous, set_previous

from time import time

from flask import Flask, render_template, url_for, jsonify
from threading import Thread
"""
Flask App for hosting API
"""
app = Flask(__name__)

# previous ping timestamp
previous_ping = get_previous()


@app.route("/")
def home():
  print("[+] OK")

  with open("rankings.txt", 'r') as file:
    file_content = file.read().split('\n')

  artists = []
  for i in file_content:
    try:
      item = i.split(" : ")
      rank = item[0]
      views = item[1]
      name = item[2]
      url = item[3]
      artists.append((rank, views, name, url))

    except Exception as e:
      print(e)
      print(f"'{i}' as {file_content.index(i)+1}th line.")

  return render_template('file.html', artists=artists)


# keep alive ping point for uptimerobot as well updates the stats twice an hour
@app.route("/refresh")
def keep_alive():
  global previous_ping

  current_ping = time()
  if current_ping - previous_ping > 2000:  # interval of 2000 seconds (approximately half an hour)
    Thread(target=main).start()
    print("[*] Updating...")
    set_previous(current_ping)

  print("[+] ping by uptimerobot")
  return jsonify({"Status": "Updating..."})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
