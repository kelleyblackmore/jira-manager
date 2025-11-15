#!/usr/bin/env python3
"""
Jira Manager CLI - Command-line interface for Jira automation.
"""

import argparse
import sys
from pathlib import Path
from jira_manager.client import JiraClient
from jira_manager.automation import AutomationManager
from jira_manager.file_manager import FileManager


def load_config(config_file: str = 'config.json') -> dict:
    """Load configuration from JSON file."""
    try:
        config = FileManager.load_json_file(config_file)
        required = ['jira_url', 'username', 'api_token']
        for field in required:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")
        return config
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        print(f"Please create a {config_file} file with jira_url, username, and api_token")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Jira Manager - Automate Jira issue creation and management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create issues from a file
  python cli.py create issues.json
  
  # Update issues from a file
  python cli.py update updates.json
  
  # Link stories to an epic
  python cli.py link link_stories.json
  
  # Get issue details
  python cli.py get PROJ-123
  
  # Search for issues
  python cli.py search "project = PROJ AND status = Open"
        """
    )
    
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create issues from JSON file')
    create_parser.add_argument('file', help='Path to JSON file with issue data')
    create_parser.add_argument('--no-save', action='store_true', 
                              help='Do not save results to file')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update issues from JSON file')
    update_parser.add_argument('file', help='Path to JSON file with update data')
    update_parser.add_argument('--no-save', action='store_true',
                              help='Do not save results to file')
    
    # Link command
    link_parser = subparsers.add_parser('link', help='Link stories to epic from JSON file')
    link_parser.add_argument('file', help='Path to JSON file with link data')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get issue details')
    get_parser.add_argument('issue_key', help='Issue key (e.g., PROJ-123)')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search issues with JQL')
    search_parser.add_argument('jql', help='JQL query string')
    search_parser.add_argument('--max', type=int, default=50,
                              help='Maximum results (default: 50)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize client
    client = JiraClient(
        base_url=config['jira_url'],
        username=config['username'],
        api_token=config['api_token']
    )
    
    # Execute commands
    try:
        if args.command == 'create':
            automation = AutomationManager(client)
            results = automation.create_issues_from_file(
                args.file, 
                save_results=not args.no_save
            )
            print(f"\nCreated {len([r for r in results if r.get('status') == 'success'])} issues")
        
        elif args.command == 'update':
            automation = AutomationManager(client)
            results = automation.update_issues_from_file(
                args.file,
                save_results=not args.no_save
            )
            print(f"\nUpdated {len([r for r in results if r.get('status') == 'success'])} issues")
        
        elif args.command == 'link':
            automation = AutomationManager(client)
            results = automation.link_stories_to_epic_from_file(args.file)
            print(f"\nLinked {len([r for r in results if r.get('status') == 'success'])} stories")
        
        elif args.command == 'get':
            issue = client.get_issue(args.issue_key)
            print(f"\nIssue: {issue['key']}")
            print(f"Type: {issue['fields']['issuetype']['name']}")
            print(f"Status: {issue['fields']['status']['name']}")
            print(f"Summary: {issue['fields']['summary']}")
            if issue['fields'].get('description'):
                desc = issue['fields']['description']
                if isinstance(desc, dict):
                    # Extract text from ADF format
                    text_content = []
                    for content in desc.get('content', []):
                        for item in content.get('content', []):
                            if item.get('type') == 'text':
                                text_content.append(item.get('text', ''))
                    print(f"Description: {' '.join(text_content)}")
                else:
                    print(f"Description: {desc}")
        
        elif args.command == 'search':
            results = client.search_issues(args.jql, max_results=args.max)
            print(f"\nFound {results['total']} issues (showing {len(results['issues'])})")
            for issue in results['issues']:
                print(f"  {issue['key']}: {issue['fields']['summary']}")
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
