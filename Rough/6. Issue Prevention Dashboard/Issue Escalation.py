import re

def should_escalate(incoming_issue):
    # Combine all tags into a single string
    tags_combined = " ".join(
        incoming_issue.get(f"tag_{i+1}", "") for i in range(9)
    ).strip()

    # Define keywords that trigger escalation
    keywords = {"urgent", "issue", "refund", "failure", "outage", "crash", "breach", "critical"}

    # Check if any keyword matches in the combined tags (case-insensitive)
    return any(re.search(rf'\b{re.escape(keyword)}\b', tags_combined, re.IGNORECASE) for keyword in keywords)
