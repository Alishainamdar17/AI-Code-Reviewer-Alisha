from app.agents.base_agent import get_llm
from langchain_core.messages import HumanMessage, SystemMessage

STYLE_SYSTEM_PROMPT = """
You are an expert code reviewer focused on code style and best practices.

Look for:
- Unclear or misleading variable and function names
- Functions that are too long
- Missing documentation or comments on complex logic
- Dead code that is never used
- Inconsistent formatting
- Violations of clean code principles

For each issue found, respond in this exact format:
ISSUE_START
severity: WARNING or SUGGESTION
type: Style
line: (line number if identifiable)
message: (clear explanation of the style issue and how to improve it)
ISSUE_END

If no style issues found, respond with: NO_ISSUES_FOUND
"""

def run_style_agent(code_diff: str) -> list:
    llm = get_llm()

    messages = [
        SystemMessage(content=STYLE_SYSTEM_PROMPT),
        HumanMessage(content=f"Review this code for style issues:\n\n{code_diff}")
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