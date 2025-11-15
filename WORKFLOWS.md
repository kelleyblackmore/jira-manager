# Jira Manager Workflow Examples

This document provides step-by-step examples of common workflows using Jira Manager.

## Workflow 1: Create a Feature with Multiple Stories

### Step 1: Create the Epic/Feature

Create a file `feature.json`:
```json
{
  "project_key": "PROJ",
  "summary": "Mobile App Authentication",
  "issue_type": "Epic",
  "epic_name": "MOBILE-AUTH",
  "description": "Implement complete authentication system for mobile app including login, logout, and password reset",
  "labels": ["mobile", "authentication", "phase-1"],
  "priority": {
    "name": "High"
  }
}
```

Run:
```bash
python cli.py create feature.json
# Output: Created PROJ-100
```

### Step 2: Create Related Stories

Create a file `stories.json`:
```json
{
  "issues": [
    {
      "project_key": "PROJ",
      "summary": "Design login screen UI",
      "issue_type": "Story",
      "description": "Create mobile-friendly login screen with email and password fields",
      "epic_key": "PROJ-100",
      "labels": ["mobile", "ui", "design"],
      "priority": {
        "name": "High"
      }
    },
    {
      "project_key": "PROJ",
      "summary": "Implement login API integration",
      "issue_type": "Story",
      "description": "Connect mobile app to backend authentication API",
      "epic_key": "PROJ-100",
      "labels": ["mobile", "backend", "api"],
      "priority": {
        "name": "High"
      }
    },
    {
      "project_key": "PROJ",
      "summary": "Add biometric authentication",
      "issue_type": "Story",
      "description": "Support fingerprint and face recognition for login",
      "epic_key": "PROJ-100",
      "labels": ["mobile", "biometric", "enhancement"],
      "priority": {
        "name": "Medium"
      }
    }
  ]
}
```

Run:
```bash
python cli.py create stories.json
# Output: 
# ✓ Created: PROJ-101 - Design login screen UI
# ✓ Created: PROJ-102 - Implement login API integration
# ✓ Created: PROJ-103 - Add biometric authentication
```

### Step 3: Update Epic Status

After stories are created, update the epic:
```json
{
  "updates": [
    {
      "issue_key": "PROJ-100",
      "labels": ["mobile", "authentication", "phase-1", "in-progress"]
    }
  ]
}
```

## Workflow 2: Bulk Import from Backlog

For large-scale imports, create a comprehensive backlog file:

```json
{
  "issues": [
    {
      "project_key": "PROJ",
      "summary": "User Management System",
      "issue_type": "Epic",
      "epic_name": "USER-MGT",
      "description": "Complete user management system"
    },
    {
      "project_key": "PROJ",
      "summary": "Create user registration",
      "issue_type": "Story",
      "description": "Allow new users to register"
    },
    {
      "project_key": "PROJ",
      "summary": "User profile editing",
      "issue_type": "Story",
      "description": "Enable users to edit their profiles"
    },
    {
      "project_key": "PROJ",
      "summary": "Password reset functionality",
      "issue_type": "Story",
      "description": "Implement forgot password flow"
    }
  ]
}
```

Run:
```bash
python cli.py create backlog.json --no-save
```

## Workflow 3: Link Existing Stories to Epic

If you have stories created without an epic:

```json
{
  "epic_key": "PROJ-100",
  "story_keys": [
    "PROJ-50",
    "PROJ-51",
    "PROJ-52",
    "PROJ-53"
  ]
}
```

Run:
```bash
python cli.py link link-to-epic.json
```

## Workflow 4: Update Multiple Issues

Bulk update for sprint planning:

```json
{
  "updates": [
    {
      "issue_key": "PROJ-101",
      "labels": ["sprint-5", "ready"],
      "priority": {
        "name": "High"
      }
    },
    {
      "issue_key": "PROJ-102",
      "labels": ["sprint-5", "ready"],
      "priority": {
        "name": "High"
      }
    },
    {
      "issue_key": "PROJ-103",
      "labels": ["backlog"],
      "priority": {
        "name": "Low"
      }
    }
  ]
}
```

Run:
```bash
python cli.py update sprint-updates.json
```

## Workflow 5: Using with CI/CD

### GitHub Actions Example

```yaml
name: Create Jira Issues

on:
  push:
    paths:
      - 'jira-issues/*.json'

jobs:
  create-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install requests
      
      - name: Create config
        run: |
          echo '{
            "jira_url": "${{ secrets.JIRA_URL }}",
            "username": "${{ secrets.JIRA_USERNAME }}",
            "api_token": "${{ secrets.JIRA_API_TOKEN }}"
          }' > config.json
      
      - name: Create Jira issues
        run: |
          for file in jira-issues/*.json; do
            python cli.py create "$file"
          done
```

## Workflow 6: Python Script Integration

```python
#!/usr/bin/env python3
from jira_manager.client import JiraClient
from jira_manager.automation import AutomationManager

# Initialize
client = JiraClient(
    base_url="https://your-domain.atlassian.net",
    username="your@email.com",
    api_token="your-token"
)

automation = AutomationManager(client)

# Create epic
epic = client.create_epic(
    project_key="PROJ",
    summary="Q4 Platform Updates",
    epic_name="Q4-PLATFORM",
    description="Platform improvements for Q4"
)

print(f"Created epic: {epic['key']}")

# Create stories from template
stories = [
    "Upgrade database to PostgreSQL 15",
    "Implement Redis caching layer",
    "Add Elasticsearch for search",
    "Optimize API response times"
]

for story_summary in stories:
    story = client.create_story(
        project_key="PROJ",
        summary=story_summary,
        epic_key=epic['key'],
        labels=["platform", "performance"]
    )
    print(f"Created story: {story['key']} - {story_summary}")
```

## Tips for Effective Usage

1. **Use Descriptive File Names**: Name your JSON files based on what they do (e.g., `sprint-5-stories.json`)

2. **Keep Results Files**: The tool saves results with `_results.json` suffix - useful for tracking what was created

3. **Test with Small Batches**: Start with a few issues to verify your field mappings work

4. **Use Labels for Organization**: Add labels to track sprints, teams, or categories

5. **Combine with Search**: Use the search command to find issues for updating

6. **Save Config Securely**: Never commit `config.json` to version control

7. **Use Environment Variables**: For CI/CD, use environment variables for credentials

8. **Validate JSON First**: Use a JSON validator before running to catch syntax errors

## Common Field Mappings

Different Jira instances may have different custom field IDs:

- **Epic Name**: Usually `customfield_10011` (configured in client.py)
- **Epic Link**: Usually `customfield_10014` or `parent` field
- **Story Points**: Usually `customfield_10016`
- **Sprint**: Usually `customfield_10020`

Check your Jira instance configuration and update field IDs as needed in the code.
