"""
Automation Manager - Automate creation and updates of Jira issues from files.
"""

import json
from typing import Dict, List, Optional
from .client import JiraClient
from .file_manager import FileManager


class AutomationManager:
    """Manager for automating Jira operations from file-based configurations."""
    
    def __init__(self, client: JiraClient):
        """
        Initialize automation manager.
        
        Args:
            client: JiraClient instance
        """
        self.client = client
        self.file_manager = FileManager()
    
    def create_issue_from_data(self, issue_data: Dict) -> Dict:
        """
        Create a single issue from data dictionary.
        
        Args:
            issue_data: Issue data containing required fields
            
        Returns:
            Created issue response
        """
        self.file_manager.validate_issue_data(issue_data)
        
        project_key = issue_data['project_key']
        summary = issue_data['summary']
        issue_type = issue_data['issue_type']
        description = issue_data.get('description')
        
        # Extract other fields
        extra_fields = {k: v for k, v in issue_data.items() 
                       if k not in ['project_key', 'summary', 'issue_type', 'description', 'epic_key']}
        
        # Handle epic-specific creation
        if issue_type.lower() == 'epic':
            epic_name = issue_data.get('epic_name', summary)
            return self.client.create_epic(
                project_key=project_key,
                summary=summary,
                epic_name=epic_name,
                description=description,
                **extra_fields
            )
        
        # Handle story creation with epic link
        elif issue_type.lower() == 'story':
            epic_key = issue_data.get('epic_key')
            return self.client.create_story(
                project_key=project_key,
                summary=summary,
                description=description,
                epic_key=epic_key,
                **extra_fields
            )
        
        # Generic issue creation
        else:
            return self.client.create_issue(
                project_key=project_key,
                summary=summary,
                issue_type=issue_type,
                description=description,
                **extra_fields
            )
    
    def create_issues_from_file(self, filepath: str, save_results: bool = True) -> List[Dict]:
        """
        Create multiple issues from a JSON file.
        
        Args:
            filepath: Path to JSON file containing issue data
            save_results: Whether to save results to a file
            
        Returns:
            List of created issue responses
        """
        data = self.file_manager.load_json_file(filepath)
        
        # Handle single issue
        if 'issues' not in data:
            result = self.create_issue_from_data(data)
            results = [result]
        else:
            # Handle bulk issues
            self.file_manager.validate_bulk_data(data)
            results = []
            
            for issue_data in data['issues']:
                try:
                    result = self.create_issue_from_data(issue_data)
                    results.append({
                        'status': 'success',
                        'data': result,
                        'input': issue_data
                    })
                    print(f"✓ Created: {result.get('key', 'N/A')} - {issue_data.get('summary', 'N/A')}")
                except Exception as e:
                    results.append({
                        'status': 'error',
                        'error': str(e),
                        'input': issue_data
                    })
                    print(f"✗ Failed: {issue_data.get('summary', 'N/A')} - {str(e)}")
        
        # Save results if requested
        if save_results:
            results_file = filepath.replace('.json', '_results.json')
            self.file_manager.save_json_file(results_file, {'results': results})
            print(f"\nResults saved to: {results_file}")
        
        return results
    
    def update_issue_from_data(self, issue_key: str, update_data: Dict) -> Dict:
        """
        Update an issue from data dictionary.
        
        Args:
            issue_key: Issue key to update
            update_data: Fields to update
            
        Returns:
            Update response
        """
        return self.client.update_issue(issue_key, **update_data)
    
    def update_issues_from_file(self, filepath: str, save_results: bool = True) -> List[Dict]:
        """
        Update multiple issues from a JSON file.
        
        Args:
            filepath: Path to JSON file containing update data
            save_results: Whether to save results to a file
            
        Returns:
            List of update responses
        """
        data = self.file_manager.load_json_file(filepath)
        
        if 'updates' not in data:
            raise ValueError("Update file must contain 'updates' key with list of updates")
        
        results = []
        for update_item in data['updates']:
            issue_key = update_item.get('issue_key')
            if not issue_key:
                results.append({
                    'status': 'error',
                    'error': 'Missing issue_key',
                    'input': update_item
                })
                continue
            
            update_fields = {k: v for k, v in update_item.items() if k != 'issue_key'}
            
            try:
                result = self.update_issue_from_data(issue_key, update_fields)
                results.append({
                    'status': 'success',
                    'issue_key': issue_key,
                    'data': result,
                    'input': update_item
                })
                print(f"✓ Updated: {issue_key}")
            except Exception as e:
                results.append({
                    'status': 'error',
                    'issue_key': issue_key,
                    'error': str(e),
                    'input': update_item
                })
                print(f"✗ Failed to update {issue_key}: {str(e)}")
        
        # Save results if requested
        if save_results:
            results_file = filepath.replace('.json', '_results.json')
            self.file_manager.save_json_file(results_file, {'results': results})
            print(f"\nResults saved to: {results_file}")
        
        return results
    
    def link_stories_to_epic_from_file(self, filepath: str) -> List[Dict]:
        """
        Link stories to an epic from a JSON file.
        
        Args:
            filepath: Path to JSON file containing link data
            
        Returns:
            List of link operation results
        """
        data = self.file_manager.load_json_file(filepath)
        
        epic_key = data.get('epic_key')
        story_keys = data.get('story_keys', [])
        
        if not epic_key:
            raise ValueError("Missing 'epic_key' in file")
        
        if not story_keys:
            raise ValueError("Missing 'story_keys' list in file")
        
        results = []
        for story_key in story_keys:
            try:
                result = self.client.link_issue_to_epic(story_key, epic_key)
                results.append({
                    'status': 'success',
                    'story_key': story_key,
                    'epic_key': epic_key,
                    'data': result
                })
                print(f"✓ Linked {story_key} to {epic_key}")
            except Exception as e:
                results.append({
                    'status': 'error',
                    'story_key': story_key,
                    'epic_key': epic_key,
                    'error': str(e)
                })
                print(f"✗ Failed to link {story_key} to {epic_key}: {str(e)}")
        
        return results
