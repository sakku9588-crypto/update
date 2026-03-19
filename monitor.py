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
    last_versions = {}
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f: last_versions = json.load(f)

    updated = False
    for repo in REPOS:
        print(f"🔍 {repo['name']} をチェック中...")
        response = requests.get(repo["url"])
        
        # 正常に取得できたかチェック
        if response.status_code != 200:
            print(f"⚠️ エラー: {repo['name']} の取得に失敗（Status: {response.status_code}）")
            print(f"メッセージ: {response.text}") # 理由を表示するニャ
            continue

        res = response.json()
        
        # tag_nameがあるかチェック
        if "tag_name" not in res:
            print(f"❌ {repo['name']} のデータに tag_name がないニャ！")
            continue

        current_ver = res["tag_name"]
        name = repo["name"]

        if name not in last_versions or last_versions[name] != current_ver:
            msg = f"🚀 **{name}** 新バージョン **[{current_ver}]** 到着！\n今すぐ `pip install -U {name}` ニャ！\n{res.get('html_url', '')}"
            requests.post(WEBHOOK_URL, json={"content": msg})
            last_versions[name] = current_ver
            updated = True

    if updated:
        with open(VERSION_FILE, "w") as f: json.dump(last_versions, f)

if __name__ == "__main__":
    check_updates()
