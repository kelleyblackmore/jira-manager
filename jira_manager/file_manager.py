"""
File Manager - Handle loading and processing of JSON files for automation.
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path


class FileManager:
    """Manager for loading and processing JSON files for Jira automation."""
    
    @staticmethod
    def load_json_file(filepath: str) -> Dict:
        """
        Load JSON data from file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Parsed JSON data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file is not valid JSON
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def save_json_file(filepath: str, data: Dict) -> None:
        """
        Save data to JSON file.
        
        Args:
            filepath: Path to JSON file
            data: Data to save
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def validate_issue_data(data: Dict) -> bool:
        """
        Validate issue data structure.
        
        Args:
            data: Issue data to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['project_key', 'summary', 'issue_type']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        return True
    
    @staticmethod
    def validate_bulk_data(data: Dict) -> bool:
        """
        Validate bulk import data structure.
        
        Args:
            data: Bulk data to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If data is invalid
        """
        if 'issues' not in data:
            raise ValueError("Bulk data must contain 'issues' key")
        
        if not isinstance(data['issues'], list):
            raise ValueError("'issues' must be a list")
        
        for idx, issue in enumerate(data['issues']):
            try:
                FileManager.validate_issue_data(issue)
            except ValueError as e:
                raise ValueError(f"Issue at index {idx} is invalid: {str(e)}")
        
        return True
