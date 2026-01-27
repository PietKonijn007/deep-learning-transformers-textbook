#!/usr/bin/env python3
"""
Final comprehensive fix for algorithm formatting in HTML files.
"""

import re
import os
from pathlib import Path

def process_algorithm_content(title, body):
    """Process algorithm body content."""
    # Remove any existing HTML formatting to start fresh
    body = re.sub(r'<div[^>]*>', '\n', body)
    body = re.sub(r'</div>', '\n', body)
    body = re.sub(r'<strong>', '', body)
    body = re.sub(r'</strong>', '', body)
    body = re.sub(r'<span[^>]*>', '', body)
    body = re.sub(r'</span>', '', body)
    
    # Clean LaTeX commands
    body = re.sub(r'\\begin\{algorithmic\}(\[\d+\])?', '', body)
    body = re.sub(r'\\end\{algorithmic\}', '', body)
    body = re.sub(r'\\State\s+', '', body)
    
    # Convert \KwIn and \KwOut
    body = re.sub(r'\\KwIn\{([^}]+)\}', r'INPUT: \1', body)
    body = re.sub(r'\\KwOut\{([^}]+)\}', r'OUTPUT: \1', body)
    
    # Convert \KwTo
    body = re.sub(r'\\KwTo\b', 'to', body)
    
    # Convert \Return
    body = re.sub(r'\\Return\{([^}]+)\}', r'return \1', body)
    
    # Convert arrow symbols
    body = re.sub(r'\\leftarrow', '←', body)
    body = re.sub(r'\\rightarrow', '→', body)
    
    # Remove line breaks
    body = re.sub(r'\\\\', '', body)
    
    # Now process line by line
    lines = body.split('\n')
    result = []
    indent_level = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip algorithmic markers
        if 'algorithmic' in line:
            continue
        
        # Check for control structures
        is_for = re.search(r'\\For\{([^}]+)\}', line)
        is_while = re.search(r'\\While\{([^}]+)\}', line)
        is_if = re.search(r'\\If\{([^}]+)\}', line)
        
        # Check for end markers
        is_end = line.strip() in ['\\EndFor', '\\EndWhile', '\\EndIf', '}']
        
        # Handle end markers - decrease indent first
        if is_end:
            if indent_level > 0:
                result.append('</div>')
                indent_level -= 1
            continue
        
        # Process control structures
        if is_for:
            condition = is_for.group(1)
            result.append(f'<div class="algorithm-line"><strong>for</strong> {condition} <strong>do</strong></div>')
            result.append('<div class="algorithm-indent">')
            indent_level += 1
        elif is_while:
            condition = is_while.group(1)
            result.append(f'<div class="algorithm-line"><strong>while</strong> {condition} <strong>do</strong></div>')
            result.append('<div class="algorithm-indent">')
            indent_level += 1
        elif is_if:
            condition = is_if.group(1)
            result.append(f'<div class="algorithm-line"><strong>if</strong> {condition} <strong>then</strong></div>')
            result.append('<div class="algorithm-indent">')
            indent_level += 1
        else:
            # Regular line - format INPUT/OUTPUT specially
            if line.startswith('INPUT:'):
                result.append(f'<div class="algorithm-line"><strong>Input:</strong> {line[6:].strip()}</div>')
            elif line.startswith('OUTPUT:'):
                result.append(f'<div class="algorithm-line"><strong>Output:</strong> {line[7:].strip()}</div>')
            elif line.startswith('return '):
                result.append(f'<div class="algorithm-line"><strong>return</strong> {line[7:]}</div>')
            elif '\\tcp{' in line:
                # Handle comments
                comment_match = re.search(r'\\tcp\{([^}]+)\}', line)
                if comment_match:
                    result.append(f'<div class="algorithm-line"><span class="algorithm-comment">// {comment_match.group(1)}</span></div>')
            else:
                result.append(f'<div class="algorithm-line">{line}</div>')
    
    # Close any remaining indent blocks
    while indent_level > 0:
        result.append('</div>')
        indent_level -= 1
    
    formatted_body = '\n'.join(result)
    return f'<div class="algorithm"><div class="algorithm-title">{title}</div>\n{formatted_body}\n</div>'

def fix_html_file(filepath):
    """Fix algorithm formatting in a single HTML file."""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find algorithm blocks more carefully - match until we find the closing </div> that matches the opening
    # We need to count div tags to find the right closing tag
    original_content = content
    
    # Find all algorithm block starts
    pattern_start = r'<div class="algorithm"><div class="algorithm-title">([^<]+)</div>'
    
    result = []
    last_end = 0
    
    for match in re.finditer(pattern_start, content):
        title = match.group(1).strip()
        start_pos = match.end()
        
        # Add content before this algorithm
        result.append(content[last_end:match.start()])
        
        # Find the matching closing </div> by counting div tags
        div_count = 1  # We're inside the algorithm div
        pos = start_pos
        while pos < len(content) and div_count > 0:
            # Look for next div tag
            next_open = content.find('<div', pos)
            next_close = content.find('</div>', pos)
            
            if next_close == -1:
                break
            
            if next_open != -1 and next_open < next_close:
                div_count += 1
                pos = next_open + 4
            else:
                div_count -= 1
                if div_count == 0:
                    # Found the matching close
                    body = content[start_pos:next_close]
                    last_end = next_close + 6  # Skip past </div>
                    break
                pos = next_close + 6
        
        # Process this algorithm block
        try:
            processed = process_algorithm_content(title, body)
            result.append(processed)
        except Exception as e:
            print(f"  ⚠ Error processing algorithm '{title}': {e}")
            # Keep original
            result.append(content[match.start():last_end])
    
    # Add remaining content
    result.append(content[last_end:])
    
    new_content = ''.join(result)
    
    if new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ Fixed algorithms")
        return True
    else:
        print(f"  - No changes needed")
        return False

def main():
    """Process all HTML files in docs and nodejs-version directories."""
    directories = ['docs/chapters', 'nodejs-version/chapters']
    
    total_fixed = 0
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory {directory} not found, skipping...")
            continue
        
        print(f"\nProcessing {directory}...")
        html_files = sorted(Path(directory).glob('*.html'))
        
        for filepath in html_files:
            if fix_html_file(filepath):
                total_fixed += 1
    
    print(f"\n✓ Complete! Fixed {total_fixed} files.")

if __name__ == '__main__':
    main()
