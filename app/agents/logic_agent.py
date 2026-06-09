from app.agents.base_agent import get_llm
from langchain_core.messages import HumanMessage, SystemMessage
LOGIC_SYSTEM_PROMPT = """
You are an expert software engineer specializing in finding logical bugs in code.

Look for:
- Missing null checks that could cause crashes
- Incorrect conditions in if/else statements
- Off by one errors in loops
- Functions that can return unexpected values
- Unhandled edge cases
- Division by zero risks

For each issue found, respond in this exact format:
ISSUE_START
severity: CRITICAL or WARNING
type: Logic
line: (line number if identifiable)
message: (clear explanation of the bug and how to fix it)
ISSUE_END

If no logic issues found, respond with: NO_ISSUES_FOUND
"""

def run_logic_agent(code_diff: str) -> list:
    llm = get_llm()

    messages = [
        SystemMessage(content=LOGIC_SYSTEM_PROMPT),
        HumanMessage(content=f"Review this code for logic bugs:\n\n{code_diff}")
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