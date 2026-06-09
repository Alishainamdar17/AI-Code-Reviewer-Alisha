from app.agents.security_agent import run_security_agent
from app.agents.logic_agent import run_logic_agent
from app.agents.style_agent import run_style_agent
from app.agents.complexity_agent import run_complexity_agent
import concurrent.futures

def run_all_agents(code_diff: str) -> list:
    all_issues = []

    print("Running all four agents in parallel...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_security   = executor.submit(run_security_agent, code_diff)
        future_logic      = executor.submit(run_logic_agent, code_diff)
        future_style      = executor.submit(run_style_agent, code_diff)
        future_complexity = executor.submit(run_complexity_agent, code_diff)

        security_issues   = future_security.result()
        logic_issues      = future_logic.result()
        style_issues      = future_style.result()
        complexity_issues = future_complexity.result()

    print(f"Security issues found:   {len(security_issues)}")
    print(f"Logic issues found:      {len(logic_issues)}")
    print(f"Style issues found:      {len(style_issues)}")
    print(f"Complexity issues found: {len(complexity_issues)}")

    all_issues.extend(security_issues)
    all_issues.extend(logic_issues)
    all_issues.extend(style_issues)
    all_issues.extend(complexity_issues)

    all_issues = sorted(all_issues, key=lambda x: (
        0 if x.get("severity") == "CRITICAL" else
        1 if x.get("severity") == "WARNING" else 2
    ))

    return all_issues

def format_review_comment(issues: list, pr_title: str) -> str:
    if not issues:
        return "## 🤖 AI Code Review\n\n✅ **No issues found!** This code looks good to merge."

    critical = [i for i in issues if i.get("severity") == "CRITICAL"]
    warnings  = [i for i in issues if i.get("severity") == "WARNING"]
    suggestions = [i for i in issues if i.get("severity") == "SUGGESTION"]

    comment = "## 🤖 AI Code Review\n\n"
    comment += f"Found **{len(issues)} issue(s)** — "
    comment += f"🔴 {len(critical)} Critical  "
    comment += f"🟡 {len(warnings)} Warnings  "
    comment += f"🟢 {len(suggestions)} Suggestions\n\n"
    comment += "---\n\n"

    if critical:
        comment += "### 🔴 Critical Issues\n\n"
        for issue in critical:
            comment += f"**{issue.get('type', 'Issue')}**"
            if issue.get('line'):
                comment += f" — Line {issue.get('line')}"
            comment += f"\n\n{issue.get('message', '')}\n\n---\n\n"

    if warnings:
        comment += "### 🟡 Warnings\n\n"
        for issue in warnings:
            comment += f"**{issue.get('type', 'Issue')}**"
            if issue.get('line'):
                comment += f" — Line {issue.get('line')}"
            comment += f"\n\n{issue.get('message', '')}\n\n---\n\n"

    if suggestions:
        comment += "### 🟢 Suggestions\n\n"
        for issue in suggestions:
            comment += f"**{issue.get('type', 'Issue')}**"
            if issue.get('line'):
                comment += f" — Line {issue.get('line')}"
            comment += f"\n\n{issue.get('message', '')}\n\n---\n\n"

    return comment