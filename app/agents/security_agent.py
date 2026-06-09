from app.agents.base_agent import get_llm
from langchain_core.messages import HumanMessage, SystemMessage
SECURITY_SYSTEM_PROMPT = """
You are an expert security code reviewer. Your job is to analyze code changes 
and find security vulnerabilities.

Look for:
- SQL injection risks (string concatenation in queries)
- Hardcoded passwords, API keys, secrets
- Unvalidated user inputs
- Insecure file handling
- Exposed sensitive data

For each issue found, respond in this exact format:
ISSUE_START
severity: CRITICAL or WARNING
type: Security
line: (line number if identifiable)
message: (clear explanation of the problem and how to fix it)
ISSUE_END

If no security issues found, respond with: NO_ISSUES_FOUND
"""

def run_security_agent(code_diff: str) -> list:
    llm = get_llm()

    messages = [
        SystemMessage(content=SECURITY_SYSTEM_PROMPT),
        HumanMessage(content=f"Review this code for security issues:\n\n{code_diff}")
    ]

    response = llm.invoke(messages)
    return parse_issues(response.content)

def parse_issues(response: str) -> list:
    issues = []

    if "NO_ISSUES_FOUND" in response:
        return issues

    blocks = response.split("ISSUE_START")
    for block in blocks[1:]:
        if "ISSUE_END" in block:
            block = block.split("ISSUE_END")[0].strip()
            issue = {}
            for line in block.strip().split("\n"):
                if line.startswith("severity:"):
                    issue["severity"] = line.replace("severity:", "").strip()
                elif line.startswith("type:"):
                    issue["type"] = line.replace("type:", "").strip()
                elif line.startswith("line:"):
                    issue["line"] = line.replace("line:", "").strip()
                elif line.startswith("message:"):
                    issue["message"] = line.replace("message:", "").strip()
            if issue:
                issues.append(issue)

    return issues