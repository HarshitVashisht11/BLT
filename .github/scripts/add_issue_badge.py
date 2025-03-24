import os
import re
import github
from github import Github

def add_badge_to_issue():
    # Get environment variables
    token = os.environ.get("GITHUB_TOKEN")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    
    if not token or not event_path:
        print("Missing required environment variables")
        return
    
    # Parse event data
    with open(event_path, "r") as f:
        import json
        event = json.load(f)
    
    # Get issue information
    repo_name = event["repository"]["full_name"]
    issue_number = event["issue"]["number"]
    issue_body = event["issue"]["body"] or ""
    
    # Check if badge already exists
    badge_pattern = r"!\[Issue Stats\]\(https:\/\/blt\.owasp\.org\/repos\/[^\/]+\/issues\/\d+\/badge\/\)"
    badge_exists = re.search(badge_pattern, issue_body)
    
    if badge_exists:
        print("Badge already exists in issue description")
        return
    
    # Create badge URL
    badge_url = f"https://blt.owasp.org/repos/{repo_name}/issues/{issue_number}/badge/"
    badge_markdown = f"\n\n![Issue Stats]({badge_url})"
    
    # Add badge to issue description
    g = Github(token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(issue_number)
    
    new_body = issue_body + badge_markdown
    issue.edit(body=new_body)
    print(f"Added badge to issue #{issue_number}")

if __name__ == "__main__":
    add_badge_to_issue()
