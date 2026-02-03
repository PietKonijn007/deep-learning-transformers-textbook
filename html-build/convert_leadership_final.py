#!/usr/bin/env python3
"""
Convert Leadership Book with full LaTeX support
Handles: tcolorbox, fbox, parbox, and all standard environments
"""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from convert_to_html import read_latex_file, process_tikz_diagrams

CHAPTERS = [
    ("preface", "Preface"),
    ("chapter01_linear_algebra", "Chapter 1: Linear Algebra Essentials"),
    ("chapter02_calculus_optimization", "Chapter 2: Calculus and Optimization"),
    ("chapter03_attention_fundamentals", "Chapter 3: Attention Fundamentals"),
    ("bridge_I_to_II", "Bridge: From Foundations to Architecture"),
    ("chapter04_training_transformers", "Chapter 4: Training Transformers"),
    ("chapter05_production_deployment", "Chapter 5: Production Deployment"),
    ("chapter06_advanced_techniques", "Chapter 6: Advanced Techniques"),
    ("bridge_II_to_III", "Bridge: From Architecture to Production"),
    ("chapter07_hardware_infrastructure", "Chapter 7: Hardware Infrastructure"),
    ("chapter08_data_pipeline", "Chapter 8: Data Pipeline"),
    ("chapter09_operationalization", "Chapter 9: Operationalization"),
    ("bridge_III_to_IV", "Bridge: From Production to Applications"),
    ("chapter10_enterprise_nlp", "Chapter 10: Enterprise NLP"),
    ("chapter11_code_tools", "Chapter 11: Code and Development Tools"),
    ("chapter12_healthcare", "Chapter 12: Healthcare Applications"),
    ("chapter13_legal", "Chapter 13: Legal and Compliance"),
    ("chapter14_finance", "Chapter 14: Financial Applications"),
    ("chapter15_autonomous_systems", "Chapter 15: Autonomous Systems"),
    ("chapter16_synthesis", "Chapter 16: Strategic Synthesis"),
    ("chapter17_frontiers", "Chapter 17: Future Frontiers"),
]

def convert_fbox_parbox(latex_content):
    """Convert \\fbox{\\parbox{...}{...}} to styled div"""
    # Pattern: \fbox{\parbox{width}{content}}
    pattern = r'\\fbox\{\\parbox\{[^}]+\}\{(.*?)\}\}'
    
    def replace_fbox(match):
        content = match.group(1).strip()
        # Remove \centering command
        content = content.replace('\\centering', '').strip()
        return f'<div class="formula-box">{content}</div>'
    
    return re.sub(pattern, replace_fbox, latex_content, flags=re.DOTALL)

def convert_tcolorbox(latex_content):
    """Convert tcolorbox environments to styled HTML divs"""
    pattern = r'\\begin\{tcolorbox\}\[([^\]]+)\](.*?)\\end\{tcolorbox\}'
    
    def replace_tcolorbox(match):
        options = match.group(1)
        content = match.group(2).strip()
        
        # Extract title
        title_match = re.search(r'title=([^,\]]+)', options)
        title = title_match.group(1) if title_match else ''
        title = title.replace('\\textbf{', '').replace('}', '')
        
        # Determine style
        box_class = 'keypoint'
        if 'blue' in options:
            box_class = 'keypoint'
        elif 'green' in options:
            box_class = 'example'
        elif 'red' in options or 'orange' in options:
            box_class = 'caution'
        
        html_box = f'<div class="{box_class}">'
        if title:
            html_box += f'<strong>{title}</strong><br>'
        html_box += content
        html_box += '</div>'
        
        return html_box
    
    return re.sub(pattern, replace_tcolorbox, latex_content, flags=re.DOTALL)

def convert_latex_to_html_enhanced(latex_content):
    """Enhanced conversion with all LaTeX box support"""
    from convert_to_html import convert_latex_to_html
    
    # Convert special boxes first (before general conversion)
    latex_content = convert_tcolorbox(latex_content)
    latex_content = convert_fbox_parbox(latex_content)
    
    # Remove LaTeX spacing and formatting commands
    latex_content = re.sub(r'\\vspace\{[^}]+\}', '', latex_content)
    latex_content = re.sub(r'\\hspace\{[^}]+\}', ' ', latex_content)
    latex_content = re.sub(r'\\noindent\s*', '', latex_content)
    
    # DON'T convert includegraphics yet - let the base converter handle the figure environment first
    
    # Use original conversion
    html_content = convert_latex_to_html(latex_content)
    
    # NOW convert includegraphics commands in the HTML output
    # At this point, the figure environment has been converted but includegraphics is still LaTeX
    def replace_graphics(match):
        options = match.group(1) if match.group(1) else ''
        path = match.group(2).strip()
        
        # Convert path: chapters/diagrams/file.pdf -> ../diagrams/file.png
        # Leadership chapters are in chapters/leadership/, diagrams are in chapters/diagrams/
        # So we need to go up one level: ../diagrams/
        if path.startswith('chapters/diagrams/'):
            path = '../diagrams/' + path[18:]  # Remove 'chapters/diagrams/' and add '../diagrams/'
        elif path.startswith('chapters/'):
            path = '../' + path[9:]  # Remove 'chapters/' and add '../'
        
        # Change extension from .pdf to .png
        if path.endswith('.pdf'):
            path = path[:-4] + '.png'
        
        return f'<img src="{path}" alt="Diagram" style="max-width: 100%; height: auto;" />'
    
    # Match \includegraphics in the HTML output
    pattern = r'\\includegraphics(?:\[([^\]]*)\])?\{([^}]+)\}'
    html_content = re.sub(pattern, replace_graphics, html_content)
    
    return html_content

def create_chapter_html(chapter_file, chapter_title, prev_chapter, next_chapter, output_dir):
    """Create HTML file with full template"""
    project_root = Path(__file__).parent.parent
    latex_path = project_root / "leadership-book/chapters" / f"{chapter_file}.tex"
    
    latex_content = read_latex_file(latex_path)
    if not latex_content:
        print(f"   ⚠️  Could not read {latex_path}")
        return
    
    # Process diagrams
    diagrams_output_dirs = [project_root / "nodejs-version/public/chapters/diagrams"]
    latex_content = process_tikz_diagrams(latex_content, chapter_file, diagrams_output_dirs)
    
    # Convert to HTML with enhanced support
    html_content = convert_latex_to_html_enhanced(latex_content)
    
    # Navigation
    nav_html = '<div class="chapter-nav">\n'
    if prev_chapter:
        nav_html += f'  <a href="{prev_chapter[0]}.html">← {prev_chapter[1]}</a>\n'
    else:
        nav_html += '  <span></span>\n'
    nav_html += '  <a href="../../leadership.html">📚 Table of Contents</a>\n'
    if next_chapter:
        nav_html += f'  <a href="{next_chapter[0]}.html">{next_chapter[1]} →</a>\n'
    else:
        nav_html += '  <span></span>\n'
    nav_html += '</div>\n'
    
    # Full HTML with complete MathJax config
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chapter_title} - Deep Learning and LLMs for Technical Leaders</title>
    <link rel="stylesheet" href="../../styles.css">
    <style>
        /* Additional styles for formula boxes */
        .formula-box {{
            background: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem auto;
            text-align: center;
            max-width: 85%;
            font-size: 1.1em;
        }}
        .formula-box p {{
            margin: 0.5rem 0;
        }}
    </style>
    <script>
    window.MathJax = {{
        tex: {{
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
            processEscapes: true,
            processEnvironments: true,
            tags: 'ams',
            packages: {{'[+]': ['ams', 'newcommand', 'configmacros']}},
            macros: {{
                R: '{{\\\\mathbb{{R}}}}', N: '{{\\\\mathbb{{N}}}}', Z: '{{\\\\mathbb{{Z}}}}', C: '{{\\\\mathbb{{C}}}}',
                vx: '{{\\\\mathbf{{x}}}}', vy: '{{\\\\mathbf{{y}}}}', vz: '{{\\\\mathbf{{z}}}}',
                vh: '{{\\\\mathbf{{h}}}}', vw: '{{\\\\mathbf{{w}}}}', vb: '{{\\\\mathbf{{b}}}}',
                vq: '{{\\\\mathbf{{q}}}}', vk: '{{\\\\mathbf{{k}}}}', vv: '{{\\\\mathbf{{v}}}}',
                mA: '{{\\\\mathbf{{A}}}}', mB: '{{\\\\mathbf{{B}}}}', mC: '{{\\\\mathbf{{C}}}}',
                mW: '{{\\\\mathbf{{W}}}}', mX: '{{\\\\mathbf{{X}}}}', mY: '{{\\\\mathbf{{Y}}}}',
                mQ: '{{\\\\mathbf{{Q}}}}', mK: '{{\\\\mathbf{{K}}}}', mV: '{{\\\\mathbf{{V}}}}',
                mH: '{{\\\\mathbf{{H}}}}', mI: '{{\\\\mathbf{{I}}}}', mU: '{{\\\\mathbf{{U}}}}', mM: '{{\\\\mathbf{{M}}}}',
                transpose: '{{^\\\\top}}', norm: ['\\\\left\\\\|#1\\\\right\\\\|', 1], abs: ['\\\\left|#1\\\\right|', 1]
            }}
        }},
        startup: {{ pageReady: () => {{ console.log('MathJax loaded'); return MathJax.startup.defaultPageReady(); }} }}
    }};
    </script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <main>{html_content}\n{nav_html}</main>
    <footer><p>&copy; 2026 Deep Learning and LLMs for Technical Leaders.</p></footer>
</body>
</html>"""
    
    output_path = output_dir / f"{chapter_file}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"   ✓ {chapter_file}.html")

def main():
    print("=" * 70)
    print("Converting Leadership Book with FULL LaTeX support")
    print("=" * 70)
    
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "nodejs-version/public/chapters/leadership"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📂 Output: {output_dir.relative_to(project_root)}")
    print(f"📝 Converting {len(CHAPTERS)} chapters...")
    print(f"   ✓ tcolorbox support")
    print(f"   ✓ fbox/parbox support")
    print(f"   ✓ All standard environments\n")
    
    for i, (chapter_file, chapter_title) in enumerate(CHAPTERS):
        prev_chapter = CHAPTERS[i-1] if i > 0 else None
        next_chapter = CHAPTERS[i+1] if i < len(CHAPTERS)-1 else None
        create_chapter_html(chapter_file, chapter_title, prev_chapter, next_chapter, output_dir)
    
    print("\n" + "=" * 70)
    print("✅ Conversion complete with FULL LaTeX support!")
    print("=" * 70)
    print("\nSupported LaTeX features:")
    print("  ✓ tcolorbox → styled divs")
    print("  ✓ fbox/parbox → formula boxes")
    print("  ✓ All theorem environments")
    print("  ✓ Tables, figures, equations")
    print("  ✓ TikZ diagrams")

if __name__ == "__main__":
    main()
