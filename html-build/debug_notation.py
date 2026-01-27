#!/usr/bin/env python3
"""Debug what's happening with notation.tex"""

import re

# Read the actual file
with open('chapters/notation.tex', 'r') as f:
    content = f.read()

# Find the first table
pattern = r'\\begin\{table\}.*?\\end\{table\}'
match = re.search(pattern, content, re.DOTALL)

if match:
    table_text = match.group(0)
    print(f"Found table, length: {len(table_text)}")
    print("="*60)
    print(table_text)
    print("="*60)
    
    # Check what comes before and after
    start_pos = match.start()
    end_pos = match.end()
    
    print(f"\n50 chars before table:")
    print(repr(content[max(0, start_pos-50):start_pos]))
    
    print(f"\n50 chars after table:")
    print(repr(content[end_pos:min(len(content), end_pos+50)]))
