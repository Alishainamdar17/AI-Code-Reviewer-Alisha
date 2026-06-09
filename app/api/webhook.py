from app.db.db_service import save_review
from fastapi import FastAPI, Request, HTTPException, Header
from dotenv import load_dotenv
from app.services.github_service import get_pr_diff, post_review_comment
from app.agents.orchestrator import run_all_agents, format_review_comment
import hashlib
import hmac
import os
import json

load_dotenv()

app = FastAPI()

def verify_signature(payload: bytes, signature: str) -> bool:
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    mac = hmac.new(
        secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256
    )
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

@app.get("/")
def root():
    return {"status": "AI Code Reviewer is running"}

@app.post("/webhook")
async def webhook(
        request: Request,
        x_hub_signature_256: str = Header(None),
        x_github_event: str = Header(None)
):
    body = await request.body()

    if not x_hub_signature_256:
        raise HTTPException(status_code=401, detail="Missing signature")

    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(body)

    print(f"\nEvent received: {x_github_event}")
    print(f"Action: {payload.get('action', 'none')}")

    if x_github_event == "pull_request":
        action = payload.get("action")
        pr_number = payload["pull_request"]["number"]
        repo_name = payload["repository"]["full_name"]
        pr_title  = payload["pull_request"]["title"]
        installation_id = payload["installation"]["id"]

        print(f"PR #{pr_number} — {pr_title} — Action: {action}")

        if action in ["opened", "synchronize"]:
            print(f"\n{'='*50}")
            print(f"Starting review for PR #{pr_number}")
            print(f"Repo: {repo_name}")
            print(f"{'='*50}")

            try:
                diff = get_pr_diff(installation_id, repo_name, pr_number)

                full_diff = ""
                for file in diff["files"]:
                    full_diff += f"\nFile: {file['filename']}\n"
                    full_diff += f"{file.get('patch', '')}\n"

                print(f"Code fetched successfully.")
                print(f"Files changed: {len(diff['files'])}")
                print(f"Running AI agents now...")

                issues = run_all_agents(full_diff)

                print(f"Agents finished. Total issues: {len(issues)}")

                review_comment = format_review_comment(issues, pr_title)

                post_review_comment(
                    installation_id,
                    repo_name,
                    pr_number,
                    issues
                )
                save_review(repo_name, pr_number, pr_title, issues)
                print(f"Review posted to GitHub successfully!")
                print(f"{'='*50}\n")

                return {
                    "status": "review posted",
                    "pr": pr_number,
                    "issues_found": len(issues)
                }

            except Exception as e:
                print(f"ERROR: {str(e)}")
                import traceback
                traceback.print_exc()
                return {"status": "error", "message": str(e)}
        else:
            print(f"Action '{action}' ignored — only processing opened/synchronize")
            return {"status": "action ignored"}

    print(f"Event '{x_github_event}' ignored")
    return {"status": "event ignored"}