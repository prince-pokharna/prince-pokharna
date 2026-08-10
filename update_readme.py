import re
import requests
from datetime import datetime, timezone

# ── CONFIG ────────────────────────────────────────────────────────────────────
USERNAME    = "prince-pokharna"
README_PATH = "README.md"

def get_github_stats():
    headers  = {"Accept": "application/vnd.github+json"}
    url      = f"https://api.github.com/users/{USERNAME}"
    response = requests.get(url, headers=headers, timeout=10)
    data     = response.json()
    public_repos = data.get("public_repos", 0)
    followers    = data.get("followers", 0)
    following    = data.get("following", 0)
    return public_repos, followers, following

def build_auto_section(public_repos, followers, following):
    now = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
    return (
        "<!-- AUTO_START -->\n"
        "> 🤖 **Auto-updated:** " + now + "\n"
        ">\n"
        "> 📦 **Public Repos:** " + str(public_repos) +
        " &nbsp;·&nbsp; 👥 **Followers:** " + str(followers) +
        " &nbsp;·&nbsp; **Following:** " + str(following) + "\n"
        "<!-- AUTO_END -->"
    )

def update_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    public_repos, followers, following = get_github_stats()
    new_section = build_auto_section(public_repos, followers, following)

    pattern = r"<!-- AUTO_START -->.*?<!-- AUTO_END -->"
    updated = re.sub(pattern, new_section, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[{now}] README updated — repos={public_repos} followers={followers}")

if __name__ == "__main__":
    update_readme()