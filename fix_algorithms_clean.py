#!/usr/bin/env python3
"""
Clean fix for algorithm formatting - converts LaTeX pseudocode to HTML.
"""

import re
import os
from pathlib import Path

def convert_algorithm_content(content):
    """Convert LaTeX algorithm pseudocode to properly formatted HTML."""
    
    # Split into lines
    lines = content.split('\n')
    result = []
    indent_level = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Handle \KwIn
        if line.startswith('\\KwIn{'):
            match = re.match(r'\\KwIn\{(.+)\}', line)
            if match:
                result.append(f'<div class="algorithm-line"><strong>Input:</strong> {match.group(1)}</div>')
                continue
        
        # Handle \KwOut
        if line.startswith('\\KwOut{'):
            match = re.match(r'\\KwOut\{(.+)\}', line)
            if match:
                result.append(f'<div class="algorithm-line"><strong>Output:</strong> {match.group(1)}</div>')
                continue
        
        # Handle \For{...}{
        if '\\For{' in line:
            match = re.search(r'\\For\{([^}]+)\}\{', line)
            if match:
                condition = match.group(1)
                # Replace \KwTo with 'to'
                condition = condition.replace('\\KwTo', 'to')
                result.append(f'<div class="algorithm-line"><strong>for</strong> {condition} <strong>do</strong></div>')
                result.append('<div class="algorithm-indent">')
                indent_level += 1
                continue
        
        # Handle \While{...}{
        if '\\While{' in line:
            match = re.search(r'\\While\{([^}]+)\}\{', line)
            if match:
                condition = match.group(1)
                result.append(f'<div class="algorithm-line"><strong>while</strong> {condition} <strong>do</strong></div>')
                result.append('<div class="algorithm-indent">')
                indent_level += 1
                continue
        
        # Handle \If{...}{
        if '\\If{' in line:
            match = re.search(r'\\If\{([^}]+)\}\{', line)
            if match:
                condition = match.group(1)
                result.append(f'<div class="algorithm-line"><strong>if</strong> {condition} <strong>then</strong></div>')
                result.append('<div class="algorithm-indent">')
                indent_level += 1
                continue
        
        # Handle closing braces
        if line == '}':
            if indent_level > 0:
                result.append('</div>')
                indent_level -= 1
            continue
        
        # Handle \Return{...}
        if '\\Return{' in line:
            match = re.search(r'\\Return\{([^}]+)\}', line)
            if match:
                result.append(f'<div class="algorithm-line"><strong>return</strong> {match.group(1)}</div>')
                continue
        
        # Handle regular lines with \\ at the end
        if line.endswith('\\\\'):
            line = line[:-2].strip()
        
        # Handle comments
        if '\\tcp{' in line:
            match = re.search(r'\\tcp\{([^}]+)\}', line)
            if match:
                result.append(f'<div class="algorithm-line"><span class="algorithm-comment">// {match.group(1)}</span></div>')
                continue
        
        # Regular line
        if line:
            result.append(f'<div class="algorithm-line">{line}</div>')
    
    # Close any remaining indent blocks
    while indent_level > 0:
        result.append('</div>')
        indent_level -= 1
    
    return '\n'.join(result)

def fix_html_file(filepath):
    """Fix algorithm formatting in a single HTML file."""
    print(f"Processing {filepath.name}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Find all algorithm blocks
    # Pattern: <div class="algorithm"><div class="algorithm-title">TITLE</div>CONTENT</div>
    pattern = r'(<div class="algorithm"><div class="algorithm-title">)([^<]+)(</div>)\s*(.*?)\s*(</div>)'
    
    def replace_algorithm(match):
        opening = match.group(1)
        title = match.group(2)
        title_close = match.group(3)
        body = match.group(4)
        closing = match.group(5)
        
        # Convert the body
        converted_body = convert_algorithm_content(body)
        
        return f'{opening}{title}{title_close}\n{converted_body}\n{closing}'
    
    content = re.sub(pattern, replace_algorithm, content, flags=re.DOTALL)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed")
        return True
    else:
        print(f"  - No changes")
        return False

def main():
    """Process all HTML files."""
    directories = ['docs/chapters', 'nodejs-version/chapters']
    
    total_fixed = 0
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory {directory} not found, skipping...")
            continue
        
        print(f"\nProcessing {directory}...")
        html_files = sorted(Path(directory).glob('chapter*.html'))
        
        for filepath in html_files:
            if fix_html_file(filepath):
                total_fixed += 1
    
    print(f"\n✓ Complete! Fixed {total_fixed} files.")

if __name__ == '__main__':
    main()
