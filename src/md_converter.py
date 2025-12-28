import markdown
import re

def markdown_to_confluence(md_content: str) -> str:
    """
    Converts Markdown content to Confluence Storage Format (XHTML).
    Handles code blocks by converting them to Confluence code macros.
    """
    
    # First, convert markdown to basic HTML
    # We use 'fenced_code' to handle standard ``` blocks
    html = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
    
    # Post-process HTML to find <pre><code> blocks and convert to Confluence Code Macro
    # Pattern to match: <pre><code( class="language-(.*?)")?>(.*?)</code></pre>
    # Note: DOTALL is needed so . matches newlines
    
    def replacer(match):
        language = match.group(1) or "text" # group 1 captures language if present
        code_content = match.group(2)
        
        # Unescape HTML entities in code content
        import html as html_lib
        code_content = html_lib.unescape(code_content)

        return (
            f'<ac:structured-macro ac:name="code" ac:schema-version="1">'
            f'<ac:parameter ac:name="language">{language}</ac:parameter>'
            f'<ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body>'
            f'</ac:structured-macro>'
        )

    # Regex to find <pre><code ...>...</code></pre>
    # Group 1: language (optional)
    # Group 2: content
    pattern = re.compile(r'<pre><code(?: class="language-(.*?)")?>(.*?)</code></pre>', re.DOTALL)
    
    confluence_storage_format = pattern.sub(replacer, html)
    
    return confluence_storage_format
