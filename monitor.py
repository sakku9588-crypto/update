import requests
import json
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
REPOS = [
    {"name": "yt-dlp", "url": "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"},
    {"name": "pytchat", "url": "https://api.github.com/repos/taizan-85/pytchat/releases/latest"}
]
VERSION_FILE = "last_versions.json"

def check_updates():
    # 前回保存したバージョンを読み込む（なければ空）
    last_versions = {}
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f: last_versions = json.load(f)

    updated = False
    for repo in REPOS:
        res = requests.get(repo["url"]).json()
        current_ver = res["tag_name"]
        name = repo["name"]

        if name not in last_versions or last_versions[name] != current_ver:
            # 新バージョン発見！Discordへ
            msg = f"🚀 **{name}** 新バージョン **[{current_ver}]** 到着！\n今すぐ `pip install -U {name}` ニャ！\n{res['html_url']}"
            requests.post(WEBHOOK_URL, json={"content": msg})
            last_versions[name] = current_ver
            updated = True

    # 更新があればファイルを保存してコミット（ここがポイントニャ）
    if updated:
        with open(VERSION_FILE, "w") as f: json.dump(last_versions, f)
        print("Updated version file.")

if __name__ == "__main__":
    check_updates()