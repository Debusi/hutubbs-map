import csv, json, requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# ジャンル定義CSVを読み込み
categories = {}
with open("board_categories.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for genre, board in reader:
        categories.setdefault(genre, []).append(board)

# 板一覧ページをスクレイピング
portal_url = "https://hutubbs.web.fc2.com/itiran.html"
res = requests.get(portal_url)
soup = BeautifulSoup(res.text, "html.parser")

board_urls = {}
for a in soup.select("a"):
    name = a.text.strip()
    href = a.get("href")
    if name and href and "jbbs.shitaraba.net" in href:
        board_urls[name] = href

# レス数集計（ダミー処理）
counts = {board: 0 for board in board_urls}

# ジャンルごとにまとめる
output = {genre: {board: counts.get(board, 0) for board in boards}
          for genre, boards in categories.items()}

with open("boards.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
