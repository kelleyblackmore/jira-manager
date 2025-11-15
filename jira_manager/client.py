"""
Jira API Client - Core client for interacting with Jira REST API.
"""

import json
import requests
from typing import Dict, List, Optional, Any


class JiraClient:
    """Client for interacting with Jira REST API using requests library."""
    
    def __init__(self, base_url: str, username: str, api_token: str):
        """
        Initialize Jira client.
        
        Args:
            base_url: Jira instance URL (e.g., https://your-domain.atlassian.net)
            username: Jira username/email
            api_token: Jira API token
        """
        self.base_url = base_url.rstrip('/')
        self.auth = (username, api_token)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict:
        """
        Make HTTP request to Jira API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: URL query parameters
            
        Returns:
            Response JSON data
            
        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}/rest/api/3/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                auth=self.auth,
                headers=self.headers,
                json=data,
                params=params
            )
            response.raise_for_status()
            
            # Some responses (like DELETE) may not have content
            if response.status_code == 204 or not response.content:
                return {}
            
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            if hasattr(e.response, 'text'):
                error_msg += f"\nResponse: {e.response.text}"
            raise Exception(error_msg)
    
    def create_issue(self, project_key: str, summary: str, issue_type: str,
                    description: Optional[str] = None, **kwargs) -> Dict:
        """
        Create a Jira issue (Story, Epic/Feature, Task, etc.).
        
        Args:
            project_key: Jira project key
            summary: Issue summary/title
            issue_type: Issue type (Story, Epic, Task, Bug, etc.)
            description: Issue description
            **kwargs: Additional fields (labels, priority, assignee, etc.)
            
        Returns:
            Created issue data
        """
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": issue_type}
            }
        }
        
        if description:
            # Using ADF (Atlassian Document Format) for description
            data["fields"]["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            }
        
        # Add any additional fields
        for key, value in kwargs.items():
            data["fields"][key] = value
        
        return self._make_request('POST', 'issue', data=data)
    
    def create_epic(self, project_key: str, summary: str, epic_name: str,
                   description: Optional[str] = None, **kwargs) -> Dict:
        """
        Create an Epic (Feature).
        
        Args:
            project_key: Jira project key
            summary: Epic summary/title
            epic_name: Epic name (for the Epic Name field)
            description: Epic description
            **kwargs: Additional fields
            
        Returns:
            Created epic data
        """
        # Add epic-specific fields
        epic_fields = {
            "customfield_10011": epic_name  # Epic Name field (may vary by instance)
        }
        epic_fields.update(kwargs)
        
        return self.create_issue(
            project_key=project_key,
            summary=summary,
            issue_type="Epic",
            description=description,
            **epic_fields
        )
    
    def create_story(self, project_key: str, summary: str,
                    description: Optional[str] = None, epic_key: Optional[str] = None,
                    **kwargs) -> Dict:
        """
        Create a Story.
        
        Args:
            project_key: Jira project key
            summary: Story summary/title
            description: Story description
            epic_key: Epic key to link this story to
            **kwargs: Additional fields
            
        Returns:
            Created story data
        """
        story_fields = {}
        if epic_key:
            # Link to epic using parent field (for next-gen projects)
            # or customfield_10014 for classic projects
            story_fields["parent"] = {"key": epic_key}
        
        story_fields.update(kwargs)
        
        return self.create_issue(
            project_key=project_key,
            summary=summary,
            issue_type="Story",
            description=description,
            **story_fields
        )
    
    def update_issue(self, issue_key: str, **fields) -> Dict:
        """
        Update an existing issue.
        
        Args:
            issue_key: Issue key (e.g., PROJ-123)
            **fields: Fields to update
            
        Returns:
            Response data
        """
        data = {"fields": fields}
        return self._make_request('PUT', f'issue/{issue_key}', data=data)
    
    def link_issue_to_epic(self, story_key: str, epic_key: str) -> Dict:
        """
        Link a story to an epic.
        
        Args:
            story_key: Story issue key
            epic_key: Epic issue key
            
        Returns:
            Response data
        """
        # Try using the parent field first (for next-gen projects)
        try:
            return self.update_issue(story_key, parent={"key": epic_key})
        except:
            # Fallback to epic link field for classic projects
            return self.update_issue(story_key, customfield_10014=epic_key)
    
    def get_issue(self, issue_key: str) -> Dict:
        """
        Get issue details.
        
        Args:
            issue_key: Issue key (e.g., PROJ-123)
            
        Returns:
            Issue data
        """
        return self._make_request('GET', f'issue/{issue_key}')
    
    def search_issues(self, jql: str, fields: Optional[List[str]] = None,
                     max_results: int = 50) -> Dict:
        """
        Search for issues using JQL.
        
        Args:
            jql: JQL query string
            fields: List of fields to return
            max_results: Maximum number of results
            
        Returns:
            Search results
        """
        params = {
            'jql': jql,
            'maxResults': max_results
        }
        if fields:
            params['fields'] = ','.join(fields)
        
        return self._make_request('GET', 'search', params=params)
    
    def add_comment(self, issue_key: str, comment_text: str) -> Dict:
        """
        Add a comment to an issue.
        
        Args:
            issue_key: Issue key
            comment_text: Comment text
            
        Returns:
            Created comment data
        """
        data = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment_text
                            }
                        ]
                    }
                ]
            }
        }
        return self._make_request('POST', f'issue/{issue_key}/comment', data=data)
