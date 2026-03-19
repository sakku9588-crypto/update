import requests
import json
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
# GitHubが自動で発行してくれる合言葉を受け取るニャ
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REPOS = [
    {"name": "yt-dlp", "url": "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"},
    {"name": "pytchat", "url": "https://api.github.com/repos/taizan-85/pytchat/releases/latest"}
]
VERSION_FILE = "last_versions.json"

def check_updates():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    last_versions = {}
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f: last_versions = json.load(f)

    updated = False
    for repo in REPOS:
        # headers={...} を追加して「公式アクセス」にするニャ
        response = requests.get(repo["url"], headers=headers)
        
        if response.status_code != 200:
            print(f"⚠️ {repo['name']} 失敗 (Status: {response.status_code})")
            continue

        res = response.json()
        if "tag_name" not in res: continue

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
