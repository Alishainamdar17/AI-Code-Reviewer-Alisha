from app.agents.base_agent import get_llm
from langchain_core.messages import HumanMessage, SystemMessage

COMPLEXITY_SYSTEM_PROMPT = """
You are an expert software architect focused on code complexity and maintainability.

Look for:
- Functions with too many nested if statements
- Functions that do too many things at once
- Code that will be very hard to maintain or modify
- Functions that are too long and should be split
- Deep nesting that makes code hard to read

For each issue found, respond in this exact format:
ISSUE_START
severity: WARNING or SUGGESTION
type: Complexity
line: (line number if identifiable)
message: (clear explanation of the complexity issue and how to simplify it)
ISSUE_END

If no complexity issues found, respond with: NO_ISSUES_FOUND
"""

def run_complexity_agent(code_diff: str) -> list:
    llm = get_llm()

    messages = [
        SystemMessage(content=COMPLEXITY_SYSTEM_PROMPT),
        HumanMessage(content=f"Review this code for complexity issues:\n\n{code_diff}")
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