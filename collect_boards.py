import csv
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 1. ジャンル定義CSVを読み込み
categories = {}
with open("board_categories.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # ヘッダ行スキップ
    for genre, board in reader:
        categories.setdefault(genre, []).append(board)

# 2. 板一覧ページをスクレイピング
portal_url = "https://hutubbs.web.fc2.com/itiran.html"
res = requests.get(portal_url)
soup = BeautifulSoup(res.text, "html.parser")

board_urls = {}
for a in soup.select("a"):
    name = a.text.strip()
    href = a.get("href")
    # したらば板リンクだけを抽出
    if name and href and "jbbs.shitaraba.net" in href:
        board_urls[name] = href

# 3. レス数集計（直近10分以内）
counts = {}
time_threshold = datetime.now() - timedelta(minutes=10)

for board, url in board_urls.items():
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        count = 0
        # 投稿一覧を抽出（HTML構造に合わせて調整必要）
        for post in soup.select(".post"):
            time_str = post.select_one(".date").text.strip()
            # 例: "2025/11/20 07:25:30"
            try:
                post_time = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
                if post_time >= time_threshold:
                    count += 1
            except Exception:
                continue
        counts[board] = count
    except Exception:
        counts[board] = 0

# 4. ジャンルごとにまとめてJSON出力
output = {
    genre: {board: counts.get(board, 0) for board in boards}
    for genre, boards in categories.items()
}

with open("boards.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("boards.json を生成しました")
