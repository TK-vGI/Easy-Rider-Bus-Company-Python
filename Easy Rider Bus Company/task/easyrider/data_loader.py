import json
from typing import List, Dict, Optional
from pathlib import Path


def load_data(file_path: Optional[str] = None) -> List[Dict]:
    """Load bus route data from a JSON file or standard input.

    Args:
        file_path: Path to the JSON file, or None for standard input.

    Returns:
        List of dictionaries containing bus route data.

    Raises:
        ValueError: If JSON is invalid.
        FileNotFoundError: If the specified file does not exist.
    """
    try:
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return json.loads(input())
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")