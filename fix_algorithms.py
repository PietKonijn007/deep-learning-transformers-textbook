#!/usr/bin/env python3
"""
Fix algorithm formatting in HTML files by converting LaTeX-style pseudocode to proper HTML.
"""

import re
import os
from pathlib import Path

def fix_algorithm_content(content):
    """Convert LaTeX-style algorithm pseudocode to HTML with proper formatting."""
    
    lines = content.split('\n')
    result = []
    indent_level = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Handle Input/Output declarations
        if line.startswith('\\KwIn{'):
            match = re.match(r'\\KwIn\{(.+?)\}', line)
            if match:
                result.append(f'<div class="algorithm-line"><strong>Input:</strong> {match.group(1)}</div>')
                continue
        
        if line.startswith('\\KwOut{'):
            match = re.match(r'\\KwOut\{(.+?)\}', line)
            if match:
                result.append(f'<div class="algorithm-line"><strong>Output:</strong> {match.group(1)}</div>')
                continue
        
        # Handle control structures
        if line.startswith('\\While{'):
            match = re.match(r'\\While\{(.+?)\}\{', line)
            if match:
                result.append(f'<div class="algorithm-line"><strong>while</strong> {match.group(1)} <strong>do</strong></div>')
                result.append('<div class="algorithm-indent">')
                indent_level += 1
                continue
        
        if line.startswith('\\For{'):
            match = re.match(r'\\For\{(.+?)\}\{', line)
            if match:
                result.append(f'<div class="algorithm-line"><strong>for</strong> {match.group(1)} <strong>do</strong></div>')
                result.append('<div class="algorithm-indent">')
                indent_level += 1
                continue
        
        if line.startswith('\\If{'):
            match = re.match(r'\\If\{(.+?)\}\{', line)
            if match:
                result.append(f'<div class="algorithm-line"><strong>if</strong> {match.group(1)} <strong>then</strong></div>')
                result.append('<div class="algorithm-indent">')
                indent_level += 1
                continue
        
        # Handle comments
        if line.startswith('\\tcp{'):
            match = re.match(r'\\tcp\{(.+?)\}', line)
            if match:
                result.append(f'<div class="algorithm-line algorithm-comment">// {match.group(1)}</div>')
                continue
        
        # Handle closing braces
        if line == '}':
            if indent_level > 0:
                result.append('</div>')
                indent_level -= 1
            continue
        
        # Handle regular lines with \\ line breaks
        if '\\\\' in line:
            # Split by \\ and process each part
            parts = line.split('\\\\')
            for part in parts:
                part = part.strip()
                if part:
                    result.append(f'<div class="algorithm-line">{part}</div>')
        else:
            # Regular line
            result.append(f'<div class="algorithm-line">{line}</div>')
    
    # Close any remaining indent blocks
    while indent_level > 0:
        result.append('</div>')
        indent_level -= 1
    
    return '\n'.join(result)

def process_algorithm_section(match):
    """Process a complete algorithm section."""
    title = match.group(1)
    body = match.group(2)
    
    # Fix the body content
    fixed_body = fix_algorithm_content(body)
    
    return f'<div class="algorithm"><div class="algorithm-title">{title}</div>\n{fixed_body}\n</div>'

def fix_html_file(filepath):
    """Fix algorithm formatting in a single HTML file."""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix all algorithm blocks
    # Pattern: <div class="algorithm"><div class="algorithm-title">...</div>...content...</div>
    pattern = r'<div class="algorithm"><div class="algorithm-title">([^<]+)</div>\s*(.*?)\s*</div>'
    
    original_content = content
    content = re.sub(pattern, process_algorithm_section, content, flags=re.DOTALL)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed algorithms in {filepath}")
        return True
    else:
        print(f"  - No changes needed in {filepath}")
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
        html_files = list(Path(directory).glob('*.html'))
        
        for filepath in html_files:
            if fix_html_file(filepath):
                total_fixed += 1
    
    print(f"\n✓ Complete! Fixed {total_fixed} files.")

if __name__ == '__main__':
    main()
