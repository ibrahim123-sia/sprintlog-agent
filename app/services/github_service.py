import logging
import requests
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com"


def get_todays_commits(repo: str, username: str, token: str) -> list:
    """Fetch today's commits by this user in a given repo."""
    since = datetime.utcnow().replace(hour=0, minute=0, second=0).isoformat() + "Z"
    url = f"{GITHUB_API_URL}/repos/{repo}/commits"
    headers = {"Authorization": f"token {token}"}
    params = {"since": since, "author": username}

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()


def get_commit_diff(repo: str, sha: str, token: str) -> str:
    """Fetch the patch/diff for a single commit."""
    url = f"{GITHUB_API_URL}/repos/{repo}/commits/{sha}"
    headers = {"Authorization": f"token {token}"}

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    files = data.get("files", [])
    diff_text = ""
    for f in files:
        diff_text += f"\nFile: {f['filename']} (+{f['additions']}/-{f['deletions']})\n"
        diff_text += f.get("patch", "")[:1500]  # truncate very long diffs
    return diff_text


def collect_daily_activity(repos: list, username: str, token: str) -> dict:
    """Main entry point: collects commits + diffs across all configured repos.

    A single misconfigured/unreachable repo shouldn't stop the other repos
    in the list from being reported on, so failures are isolated per repo.
    """
    activity = {"repos": {}, "total_commits": 0}

    for repo in repos:
        try:
            commits = get_todays_commits(repo, username, token)
        except requests.RequestException:
            logger.warning("Skipping repo %r — failed to fetch commits", repo, exc_info=True)
            continue

        repo_data = []
        for c in commits:
            sha = c["sha"]
            message = c["commit"]["message"]
            try:
                diff = get_commit_diff(repo, sha, token)
            except requests.RequestException:
                logger.warning("Skipping commit %s in %r — failed to fetch diff", sha[:7], repo, exc_info=True)
                diff = ""
            repo_data.append({"sha": sha[:7], "message": message, "diff": diff})

        if repo_data:
            activity["repos"][repo] = repo_data
            activity["total_commits"] += len(repo_data)

    return activity