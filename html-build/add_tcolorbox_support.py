#!/usr/bin/env python3
"""
Add tcolorbox support to convert_latex_to_html function
This patches the conversion to handle tcolorbox environments
"""

import re

def convert_tcolorbox(html_content):
    """Convert tcolorbox environments to styled HTML divs"""
    
    # Pattern to match tcolorbox with options and title
    # \begin{tcolorbox}[colback=blue!5!white,colframe=blue!75!black,title=TITLE]
    pattern = r'\\begin\{tcolorbox\}\[([^\]]+)\](.*?)\\end\{tcolorbox\}'
    
    def replace_tcolorbox(match):
        options = match.group(1)
        content = match.group(2).strip()
        
        # Extract title if present
        title_match = re.search(r'title=([^,\]]+)', options)
        title = title_match.group(1) if title_match else ''
        
        # Clean up title (remove LaTeX formatting)
        title = title.replace('\\textbf{', '').replace('}', '')
        
        # Determine box style based on color
        box_class = 'keypoint'  # default
        if 'blue' in options:
            box_class = 'keypoint'
        elif 'green' in options:
            box_class = 'example'
        elif 'red' in options or 'orange' in options:
            box_class = 'caution'
        
        # Build HTML
        html_box = f'<div class="{box_class}">'
        if title:
            html_box += f'<strong>{title}</strong><br>'
        html_box += content
        html_box += '</div>'
        
        return html_box
    
    # Apply conversion
    html_content = re.sub(pattern, replace_tcolorbox, html_content, flags=re.DOTALL)
    
    return html_content

# Test the function
if __name__ == "__main__":
    test_latex = r"""
\begin{tcolorbox}[colback=blue!5!white,colframe=blue!75!black,title=MENTAL MODEL: Cost Driver Dominance]
Principle: In any ML system, 80% of costs come from 20% of operations.
\end{tcolorbox}
"""
    
    result = convert_tcolorbox(test_latex)
    print("Input:")
    print(test_latex)
    print("\nOutput:")
    print(result)
