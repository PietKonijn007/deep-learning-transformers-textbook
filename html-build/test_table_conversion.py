#!/usr/bin/env python3
"""Test table conversion to debug the issue"""

import re

# Sample LaTeX table from notation.tex - EXACT copy
test_latex = r"""\begin{table}[htbp]
\centering
\begin{tabular}{cl}
\toprule
\textbf{Symbol} & \textbf{Meaning} \\
\midrule
$a, b, c$ & Scalars (lowercase italic) \\
$n, m, d$ & Integer scalars (dimensions, indices) \\
\bottomrule
\end{tabular}
\caption{General mathematical notation conventions}
\end{table}"""

print("Original LaTeX:")
print(test_latex)
print("\n" + "="*60 + "\n")

# Test the NEW conversion function
def convert_table_environment(match):
    """Convert entire table environment including wrapper and tabular"""
    full_content = match.group(0)
    
    # Extract just the tabular content
    tabular_match = re.search(r'\\begin\{tabular\}\{[^}]+\}(.*?)\\end\{tabular\}', full_content, re.DOTALL)
    if not tabular_match:
        return full_content
    
    table_content = tabular_match.group(1)
    
    print(f"Table content before cleanup:\n{repr(table_content[:200])}\n")
    
    # Remove all booktabs and table formatting commands with surrounding whitespace
    table_content = re.sub(r'\s*\\toprule\s*', '\n', table_content)
    table_content = re.sub(r'\s*\\midrule\s*', '\n', table_content)
    table_content = re.sub(r'\s*\\bottomrule\s*', '\n', table_content)
    table_content = re.sub(r'\s*\\hline\s*', '\n', table_content)
    
    print(f"Table content after cleanup:\n{repr(table_content[:200])}\n")
    
    # Split by \\ for rows
    rows = [r.strip() for r in table_content.split('\\\\') if r.strip()]
    
    print(f"Rows after split: {len(rows)}")
    for i, row in enumerate(rows):
        print(f"  Row {i}: {repr(row[:80])}")
    
    html_rows = []
    
    for i, row in enumerate(rows):
        row = row.strip()
        if not row:
            continue
        
        # Skip rows that are just whitespace or booktabs commands
        if not row or re.match(r'^\\(toprule|midrule|bottomrule|hline)\s*$', row):
            continue
        
        # Split by &
        cells = [c.strip() for c in row.split('&')]
        
        # First row is typically the header
        if i == 0:
            html_rows.append('<tr>' + ''.join(f'<th>{cell}</th>' for cell in cells) + '</tr>')
        else:
            html_rows.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>')
    
    return '\n<table>\n' + '\n'.join(html_rows) + '\n</table>\n'

# Apply the conversion
pattern = r'\\begin\{table\}.*?\\end\{table\}'
result = re.sub(pattern, convert_table_environment, test_latex, flags=re.DOTALL)

print("\n" + "="*60 + "\n")
print("Result:")
print(result)
