# Quick Start Guide

Get up and running with Jira Manager in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/kelleyblackmore/jira-manager.git
cd jira-manager

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create your configuration file:
```bash
cp examples/config.example.json config.json
```

2. Edit `config.json` with your credentials:
```json
{
  "jira_url": "https://your-domain.atlassian.net",
  "username": "your-email@example.com",
  "api_token": "your-api-token"
}
```

**Getting an API Token:**
- Go to: https://id.atlassian.com/manage-profile/security/api-tokens
- Click "Create API token"
- Copy the token and paste it in `config.json`

## Your First Issue

Create a file `my-first-issue.json`:
```json
{
  "project_key": "PROJ",
  "summary": "My first automated issue",
  "issue_type": "Task",
  "description": "Created using Jira Manager!"
}
```

Replace `PROJ` with your actual Jira project key.

Run:
```bash
python cli.py create my-first-issue.json
```

✅ Done! Check your Jira project to see the new issue.

## Create an Epic with Stories

1. Create the epic (`my-epic.json`):
```json
{
  "project_key": "PROJ",
  "summary": "Mobile App Phase 1",
  "issue_type": "Epic",
  "epic_name": "MOBILE-P1",
  "description": "First phase of mobile app development"
}
```

2. Create it:
```bash
python cli.py create my-epic.json
# Note the epic key (e.g., PROJ-100)
```

3. Create stories (`my-stories.json`):
```json
{
  "issues": [
    {
      "project_key": "PROJ",
      "summary": "Design login screen",
      "issue_type": "Story",
      "epic_key": "PROJ-100",
      "description": "Create mobile login UI"
    },
    {
      "project_key": "PROJ",
      "summary": "Implement authentication",
      "issue_type": "Story",
      "epic_key": "PROJ-100",
      "description": "Backend authentication logic"
    }
  ]
}
```

Replace `PROJ-100` with your actual epic key.

4. Create the stories:
```bash
python cli.py create my-stories.json
```

✅ You now have an epic with linked stories!

## Common Commands

```bash
# Create issues from file
python cli.py create issues.json

# Update issues
python cli.py update updates.json

# Link stories to epic
python cli.py link link-stories.json

# Get issue details
python cli.py get PROJ-123

# Search issues
python cli.py search "project = PROJ AND status = Open"
```

## Using as Python Library

```python
from jira_manager.client import JiraClient

# Initialize client
client = JiraClient(
    base_url="https://your-domain.atlassian.net",
    username="your@email.com",
    api_token="your-token"
)

# Create an issue
issue = client.create_issue(
    project_key="PROJ",
    summary="My issue",
    issue_type="Task"
)

print(f"Created: {issue['key']}")
```

## Next Steps

- See [README.md](README.md) for complete documentation
- Check [WORKFLOWS.md](WORKFLOWS.md) for detailed workflow examples
- Explore the `examples/` directory for more examples

## Troubleshooting

**"Authentication failed"**
- Verify your API token is correct
- Ensure username is the email address for your Jira account
- Check that `jira_url` includes `https://`

**"Project does not exist"**
- Verify the project key is correct
- Ensure you have access to the project

**"Field does not exist"**
- Epic field IDs may vary by Jira instance
- Check your Jira admin settings for custom field IDs

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review [WORKFLOWS.md](WORKFLOWS.md) for examples
- Open an issue on GitHub if you need help

---

**Happy automating! 🚀**
