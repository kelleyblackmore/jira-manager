# Jira Manager

A Python tool for interacting with the Jira API using only the `requests` library. This tool enables automated creation and management of Jira issues (Features/Epics, Stories, Tasks, etc.) through simple JSON files.

## Features

- 🚀 **Simple API Client**: Pure Python implementation using only the `requests` library
- 📝 **File-based Automation**: Define issues in JSON files for easy automation
- 🎯 **Epic/Feature Management**: Create epics and link stories to them
- 📦 **Bulk Operations**: Create or update multiple issues at once
- 🔄 **Update Issues**: Modify existing issues with new data
- 🔗 **Link Stories to Epics**: Automatically associate stories with features
- 💻 **CLI Interface**: Command-line tool for easy integration with scripts and CI/CD

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kelleyblackmore/jira-manager.git
cd jira-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create your configuration file:
```bash
cp examples/config.example.json config.json
```

4. Edit `config.json` with your Jira credentials:
```json
{
  "jira_url": "https://your-domain.atlassian.net",
  "username": "your-email@example.com",
  "api_token": "your-api-token-here"
}
```

### Getting a Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name and copy the token
4. Use this token in your `config.json`

## Usage

### Command-Line Interface

#### Create Issues from File

Create a single issue:
```bash
python cli.py create examples/create_epic.json
```

Create multiple issues at once:
```bash
python cli.py create examples/bulk_create.json
```

#### Update Existing Issues

```bash
python cli.py update examples/update_issues.json
```

#### Link Stories to Epic

```bash
python cli.py link examples/link_stories_to_epic.json
```

#### Get Issue Details

```bash
python cli.py get PROJ-123
```

#### Search Issues with JQL

```bash
python cli.py search "project = PROJ AND status = Open"
python cli.py search "assignee = currentUser()" --max 100
```

### Using as a Python Library

```python
from jira_manager.client import JiraClient
from jira_manager.automation import AutomationManager

# Initialize client
client = JiraClient(
    base_url="https://your-domain.atlassian.net",
    username="your-email@example.com",
    api_token="your-api-token"
)

# Create an epic
epic = client.create_epic(
    project_key="PROJ",
    summary="User Authentication Feature",
    epic_name="AUTH-001",
    description="Implement user authentication system"
)
print(f"Created epic: {epic['key']}")

# Create a story linked to the epic
story = client.create_story(
    project_key="PROJ",
    summary="Implement login API",
    description="Create REST API endpoint for user login",
    epic_key=epic['key']
)
print(f"Created story: {story['key']}")

# Update an issue
client.update_issue("PROJ-123", summary="Updated summary")

# Search for issues
results = client.search_issues("project = PROJ AND status = Open")
for issue in results['issues']:
    print(f"{issue['key']}: {issue['fields']['summary']}")

# Use automation for file-based operations
automation = AutomationManager(client)
results = automation.create_issues_from_file("my_issues.json")
```

## JSON File Formats

### Single Epic/Feature

```json
{
  "project_key": "PROJ",
  "summary": "User Authentication Feature",
  "issue_type": "Epic",
  "epic_name": "AUTH-001",
  "description": "Implement user authentication system",
  "labels": ["authentication", "security"],
  "priority": {
    "name": "High"
  }
}
```

### Single Story

```json
{
  "project_key": "PROJ",
  "summary": "Implement login API endpoint",
  "issue_type": "Story",
  "description": "Create REST API endpoint for user login",
  "epic_key": "PROJ-1",
  "labels": ["backend", "api"],
  "priority": {
    "name": "High"
  }
}
```

### Bulk Create Multiple Issues

```json
{
  "issues": [
    {
      "project_key": "PROJ",
      "summary": "First Issue",
      "issue_type": "Story",
      "description": "Description here"
    },
    {
      "project_key": "PROJ",
      "summary": "Second Issue",
      "issue_type": "Task",
      "description": "Another description"
    }
  ]
}
```

### Update Issues

```json
{
  "updates": [
    {
      "issue_key": "PROJ-123",
      "summary": "Updated summary",
      "labels": ["updated", "in-progress"]
    },
    {
      "issue_key": "PROJ-124",
      "priority": {
        "name": "High"
      }
    }
  ]
}
```

### Link Stories to Epic

```json
{
  "epic_key": "PROJ-1",
  "story_keys": [
    "PROJ-10",
    "PROJ-11",
    "PROJ-12"
  ]
}
```

## API Reference

### JiraClient

Main client for interacting with Jira REST API.

#### Methods

- `create_issue(project_key, summary, issue_type, description=None, **kwargs)` - Create any type of issue
- `create_epic(project_key, summary, epic_name, description=None, **kwargs)` - Create an Epic/Feature
- `create_story(project_key, summary, description=None, epic_key=None, **kwargs)` - Create a Story
- `update_issue(issue_key, **fields)` - Update an existing issue
- `link_issue_to_epic(story_key, epic_key)` - Link a story to an epic
- `get_issue(issue_key)` - Get issue details
- `search_issues(jql, fields=None, max_results=50)` - Search issues using JQL
- `add_comment(issue_key, comment_text)` - Add a comment to an issue

### AutomationManager

Manager for file-based automation.

#### Methods

- `create_issue_from_data(issue_data)` - Create issue from dictionary
- `create_issues_from_file(filepath, save_results=True)` - Create issues from JSON file
- `update_issue_from_data(issue_key, update_data)` - Update issue from dictionary
- `update_issues_from_file(filepath, save_results=True)` - Update issues from JSON file
- `link_stories_to_epic_from_file(filepath)` - Link stories to epic from JSON file

## Examples

See the `examples/` directory for complete examples:

- `create_epic.json` - Create a single epic/feature
- `create_story.json` - Create a single story
- `bulk_create.json` - Create multiple issues at once
- `update_issues.json` - Update existing issues
- `link_stories_to_epic.json` - Link stories to an epic

## Automation Workflows

### Create a Feature with Stories

1. Create the epic:
```bash
python cli.py create examples/create_epic.json
# Output: Created PROJ-1
```

2. Update story files with the epic key (`PROJ-1`)

3. Create the stories:
```bash
python cli.py create examples/bulk_create.json
```

### Update Multiple Features

1. Create `updates.json` with all changes
2. Run:
```bash
python cli.py update updates.json
```

## Integration with CI/CD

You can integrate this tool with your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Create Jira Issues
  run: |
    pip install -r requirements.txt
    python cli.py create issues.json
  env:
    JIRA_URL: ${{ secrets.JIRA_URL }}
    JIRA_USER: ${{ secrets.JIRA_USER }}
    JIRA_TOKEN: ${{ secrets.JIRA_TOKEN }}
```

## Reference

This tool is inspired by the Jira JSON import format:
https://confluence.atlassian.com/adminjiraserver/importing-data-from-json-938847609.html

## Troubleshooting

### Authentication Errors
- Verify your API token is correct
- Ensure your username is the email associated with your Jira account
- Check that your Jira URL is correct (include https://)

### Field Errors
- Epic Name field ID (`customfield_10011`) may vary by Jira instance
- Parent field may not be available in classic projects (use `customfield_10014` instead)
- Check your project's custom fields configuration

### Permission Errors
- Ensure your account has permission to create issues in the project
- Verify you have permission to create Epics (may require specific role)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.