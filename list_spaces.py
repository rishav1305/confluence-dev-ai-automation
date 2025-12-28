import argparse
import sys
import os
from dotenv import load_dotenv
from src.confluence_client import ConfluenceClient

# Load environment variables from .env file
load_dotenv()

def main():
    try:
        client = ConfluenceClient()
        print(f"Connecting to Confluence at {client.url}...")
        
        spaces = client.confluence.get_all_spaces(start=0, limit=5, expand='description.plain,body.view')
        print("Available Spaces:")
        for space in spaces.get('results', []):
            print(f"- {space['name']} (Key: {space['key']})")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
