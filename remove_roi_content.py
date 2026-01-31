#!/usr/bin/env python3
"""
Remove ROI and business impact content from chapters 24-34
"""
import re
import glob

def remove_roi_content(text):
    """Remove various forms of ROI and business impact content"""
    
    # Remove "Business Impact:" paragraphs
    text = re.sub(
        r'\\textbf\{Business Impact:\}[^\n]*\n\n',
        '',
        text,
        flags=re.DOTALL
    )
    
    # Remove ROI calculations and mentions
    text = re.sub(
        r'ROI:\s*[^\n]*\n',
        '',
        text
    )
    
    # Remove payback period mentions
    text = re.sub(
        r'[Pp]ayback period:\s*[^\n]*\n',
        '',
        text
    )
    
    # Remove dollar amount calculations with ROI context
    text = re.sub(
        r'\.\s*At \$[^.]*\$[^.]*\.\s*ROI:[^\n]*',
        '.',
        text
    )
    
    # Remove business impact sentences
    text = re.sub(
        r'The business impact[^.]*\.',
        '',
        text
    )
    
    # Remove cost management and ROI tracking paragraphs
    text = re.sub(
        r'\\textbf\{Cost management and ROI tracking\.\}[^}]*\}[^\n]*\n\n',
        '',
        text,
        flags=re.DOTALL
    )
    
    return text

# Process each chapter
chapters_to_process = [
    'chapters/chapter24_domain_specific_models.tex',
    'chapters/chapter25_enterprise_nlp.tex',
    'chapters/chapter26_code_language.tex',
    'chapters/chapter28_knowledge_graphs.tex',
    'chapters/chapter31_finance.tex',
    'chapters/chapter32_legal.tex',
    'chapters/chapter33_observability.tex',
    'chapters/chapter34_dsl_agents.tex',
]

for filepath in chapters_to_process:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_length = len(content)
        cleaned_content = remove_roi_content(content)
        removed_length = original_length - len(cleaned_content)
        
        if removed_length > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"✓ {filepath}: Removed {removed_length} characters")
        else:
            print(f"- {filepath}: No changes needed")
            
    except FileNotFoundError:
        print(f"✗ {filepath}: File not found")
    except Exception as e:
        print(f"✗ {filepath}: Error - {e}")

print("\nDone!")
