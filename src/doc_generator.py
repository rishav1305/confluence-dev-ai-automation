import argparse
import sys
import os
from dotenv import load_dotenv
from src.confluence_client import ConfluenceClient
from src.md_converter import markdown_to_confluence

# Load environment variables from .env file
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Generate documentation in Confluence.")
    parser.add_argument("--space", required=True, help="Confluence Space Key")
    parser.add_argument("--title", required=True, help="Page Title")
    parser.add_argument("--content", required=True, help="Page Content (Storage Format or Markdown)")
    parser.add_argument("--parent", help="Parent Page ID (Optional)", default=None)
    parser.add_argument("--markdown", action="store_true", help="Treat content as Markdown and convert to Storage Format")

    args = parser.parse_args()

    try:
        content = args.content
        if args.markdown:
            print("Converting Markdown to Confluence Storage Format...")
            content = markdown_to_confluence(content)

        client = ConfluenceClient()
        
        print(f"Connecting to Confluence at {client.url}...")
        
        if client.page_exists(args.space, args.title):
            print(f"Page '{args.title}' already exists in space '{args.space}'. Updating...")
            page_id = client.get_page_id(args.space, args.title)
            if page_id:
                client.update_page(page_id, args.title, content)
                print(f"Successfully updated page {page_id}.")
            else:
                print("Error: Page exists but ID could not be retrieved.")
        else:
            print(f"Creating new page '{args.title}' in space '{args.space}'...")
            result = client.create_page(args.space, args.title, content, args.parent)
            print(f"Successfully created page with ID: {result.get('id')}")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
