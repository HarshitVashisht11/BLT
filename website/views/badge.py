import datetime
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from website.models import IP, GithubIssue
import json
import requests

def create_badge(color, label, message):
    """Create a badge using shields.io service"""
    url = f"https://img.shields.io/badge/{label}-{message}-{color}"
    response = requests.get(url)
    return response.content

def issue_badge(request, repo_name, issue_number):
    """Generate a badge for an issue with view count and bounty"""
    # Get the issue
    try:
        github_issue = GithubIssue.objects.filter(
            issue__url__contains=f"/{repo_name}/issues/{issue_number}"
        ).first()
        
        if not github_issue:
            return HttpResponse("Issue not found", status=404)
            
        issue = github_issue.issue
        
        # Get view count for the past 30 days
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        view_count = IP.objects.filter(
            issue=issue,
            created__gte=thirty_days_ago
        ).count()
        
        # Get bounty amount
        bounty_amount = github_issue.bounty if github_issue.bounty else 0
        
        # Create badge content
        label = "Issue+Stats"
        message = f"{view_count}+views+%7C+${bounty_amount}+bounty"
        color = "blue"
        
        badge_svg = create_badge(color, label, message)
        
        # Return the badge as SVG
        return HttpResponse(badge_svg, content_type="image/svg+xml")
        
    except Exception as e:
        print(f"Error generating badge: {e}")
        return HttpResponse("Error generating badge", status=500)
