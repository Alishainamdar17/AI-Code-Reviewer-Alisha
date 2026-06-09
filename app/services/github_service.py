from github import GithubIntegration, Github
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

def get_github_client(installation_id: int):
    integration = GithubIntegration(APP_ID, PRIVATE_KEY)
    token = integration.get_access_token(installation_id).token
    return Github(token)

def get_pr_diff(installation_id: int, repo_name: str, pr_number: int):
    client = get_github_client(installation_id)
    repo = client.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    files_changed = []
    for file in pr.get_files():
        files_changed.append({
            "filename": file.filename,
            "status": file.status,
            "additions": file.additions,
            "deletions": file.deletions,
            "patch": file.patch
        })

    return {
        "pr_number": pr_number,
        "repo": repo_name,
        "title": pr.title,
        "description": pr.body,
        "files": files_changed
    }

def post_review_comment(installation_id: int, repo_name: str, pr_number: int, comments: list):
    client = get_github_client(installation_id)
    repo = client.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    body = "## 🤖 AI Code Review\n\n"
    for comment in comments:
        severity = comment.get("severity", "INFO")
        if severity == "CRITICAL":
            emoji = "🔴"
        elif severity == "WARNING":
            emoji = "🟡"
        else:
            emoji = "🟢"

        body += f"{emoji} **{severity}** — {comment.get('type', '')}\n\n"
        body += f"{comment.get('message', '')}\n\n"
        body += "---\n\n"

    pr.create_issue_comment(body)
    print(f"Review posted on PR #{pr_number}")