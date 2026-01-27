#!/usr/bin/env python3
"""
Comprehensive fix for algorithm formatting in HTML files.
Converts LaTeX-style pseudocode to properly formatted HTML.
"""

import re
import os
from pathlib import Path

def clean_latex_commands(text):
    """Remove or convert LaTeX commands to plain text/HTML."""
    # Remove algorithmic environment markers
    text = re.sub(r'\\begin\{algorithmic\}(\[\d+\])?', '', text)
    text = re.sub(r'\\end\{algorithmic\}', '', text)
    
    # Convert \State to nothing (just the content)
    text = re.sub(r'\\State\s+', '', text)
    
    # Convert \For, \EndFor, \While, \EndWhile, etc.
    text = re.sub(r'\\For\{([^}]+)\}', r'<strong>for</strong> \1 <strong>do</strong>', text)
    text = re.sub(r'\\EndFor', '', text)
    text = re.sub(r'\\While\{([^}]+)\}', r'<strong>while</strong> \1 <strong>do</strong>', text)
    text = re.sub(r'\\EndWhile', '', text)
    text = re.sub(r'\\If\{([^}]+)\}', r'<strong>if</strong> \1 <strong>then</strong>', text)
    text = re.sub(r'\\EndIf', '', text)
    
    # Convert \KwIn and \KwOut - handle both with and without closing braces
    text = re.sub(r'\\KwIn\{([^}]+)\}', r'<strong>Input:</strong> \1', text)
    text = re.sub(r'\\KwOut\{([^}]+)\}', r'<strong>Output:</strong> \1', text)
    
    # Convert \KwTo
    text = re.sub(r'\\KwTo\b', 'to', text)
    
    # Convert comments
    text = re.sub(r'\\tcp\{([^}]+)\}', r'<span class="algorithm-comment">// \1</span>', text)
    
    # Convert \Return with and without braces
    text = re.sub(r'\\Return\{([^}]+)\}', r'<strong>return</strong> \1', text)
    text = re.sub(r'\\Return\b', r'<strong>return</strong>', text)
    
    # Remove leftover backslashes from line breaks
    text = re.sub(r'\\\\', '', text)
    
    # Clean up any remaining common LaTeX commands
    text = re.sub(r'\\leftarrow', '←', text)
    text = re.sub(r'\\rightarrow', '→', text)
    
    return text

def detect_indent_level(line):
    """Detect indentation level based on control structures."""
    line = line.strip()
    
    # Increase indent after these
    if any(keyword in line for keyword in ['<strong>for</strong>', '<strong>while</strong>', '<strong>if</strong>']):
        return 'increase'
    
    # Decrease indent for these (but they should be at current level)
    if line.startswith('\\EndFor') or line.startswith('\\EndWhile') or line.startswith('\\EndIf'):
        return 'decrease'
    
    return 'same'

def format_algorithm_content(content):
    """Format algorithm content with proper HTML structure."""
    # Clean LaTeX commands first
    content = clean_latex_commands(content)
    
    lines = content.split('\n')
    result = []
    indent_level = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip empty algorithmic markers
        if line in ['\\begin{algorithmic}', '\\end{algorithmic}', '\\begin{algorithmic}[1]']:
            continue
        
        # Handle indent changes
        indent_change = detect_indent_level(line)
        
        # Decrease indent before adding the line for end markers
        if indent_change == 'decrease':
            if indent_level > 0:
                result.append('</div>')
                indent_level -= 1
            continue  # Don't add EndFor/EndWhile/EndIf lines
        
        # Add the line
        result.append(f'<div class="algorithm-line">{line}</div>')
        
        # Increase indent after adding the line for control structures
        if indent_change == 'increase':
            result.append('<div class="algorithm-indent">')
            indent_level += 1
    
    # Close any remaining indent blocks
    while indent_level > 0:
        result.append('</div>')
        indent_level -= 1
    
    return '\n'.join(result)

def process_algorithm_block(match):
    """Process a complete algorithm block."""
    title = match.group(1).strip()
    body = match.group(2).strip()
    
    # Format the body
    formatted_body = format_algorithm_content(body)
    
    return f'<div class="algorithm"><div class="algorithm-title">{title}</div>\n{formatted_body}\n</div>'

def fix_html_file(filepath):
    """Fix algorithm formatting in a single HTML file."""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix all algorithm blocks
    pattern = r'<div class="algorithm"><div class="algorithm-title">([^<]+)</div>\s*(.*?)\s*</div>'
    
    original_content = content
    
    # Process each algorithm block
    def replace_func(match):
        try:
            return process_algorithm_block(match)
        except Exception as e:
            print(f"  ⚠ Error processing algorithm: {e}")
            return match.group(0)  # Return original if error
    
    content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    
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
        html_files = sorted(Path(directory).glob('*.html'))
        
        for filepath in html_files:
            if fix_html_file(filepath):
                total_fixed += 1
    
    print(f"\n✓ Complete! Fixed {total_fixed} files.")

if __name__ == '__main__':
    main()
