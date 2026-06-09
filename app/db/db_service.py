from app.db.models import PullRequest, Review, Issue
from app.db.database import SessionLocal

def save_review(repo_name: str, pr_number: int, pr_title: str, issues: list):
    db = SessionLocal()
    try:
        pr = PullRequest(
            repo_name=repo_name,
            pr_number=pr_number,
            pr_title=pr_title,
            status="reviewed"
        )
        db.add(pr)
        db.flush()

        critical    = len([i for i in issues if i.get("severity") == "CRITICAL"])
        warnings    = len([i for i in issues if i.get("severity") == "WARNING"])
        suggestions = len([i for i in issues if i.get("severity") == "SUGGESTION"])

        review = Review(
            pull_request_id  = pr.id,
            total_issues     = len(issues),
            critical_count   = critical,
            warning_count    = warnings,
            suggestion_count = suggestions
        )
        db.add(review)
        db.flush()

        for issue in issues:
            db_issue = Issue(
                review_id   = review.id,
                severity    = issue.get("severity", "INFO"),
                issue_type  = issue.get("type", "General"),
                message     = issue.get("message", ""),
                line_number = issue.get("line", "")
            )
            db.add(db_issue)

        db.commit()
        print(f"Review saved to database — PR #{pr_number} — {len(issues)} issues")

    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
    finally:
        db.close()