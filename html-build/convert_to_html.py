#!/usr/bin/env python3
"""
Convert LaTeX textbook to HTML with MathJax support
"""

import os
import re
import sys
from pathlib import Path

# Chapter information
CHAPTERS = [
    ("preface", "Preface"),
    ("notation", "Notation and Conventions"),
    ("chapter01_linear_algebra", "Chapter 1: Linear Algebra for Deep Learning"),
    ("chapter02_calculus_optimization", "Chapter 2: Calculus and Optimization"),
    ("chapter03_probability_information", "Chapter 3: Probability and Information Theory"),
    ("chapter04_feedforward_networks", "Chapter 4: Feed-Forward Neural Networks"),
    ("chapter05_convolutional_networks", "Chapter 5: Convolutional Neural Networks"),
    ("chapter06_recurrent_networks", "Chapter 6: Recurrent Neural Networks"),
    ("chapter07_attention_fundamentals", "Chapter 7: Attention Mechanisms: Fundamentals"),
    ("chapter08_self_attention", "Chapter 8: Self-Attention and Multi-Head Attention"),
    ("chapter09_attention_variants", "Chapter 9: Attention Variants and Mechanisms"),
    ("chapter10_transformer_model", "Chapter 10: The Transformer Model"),
    ("chapter11_training_transformers", "Chapter 11: Training Transformers"),
    ("chapter12_computational_analysis", "Chapter 12: Computational Analysis"),
    ("chapter13_bert", "Chapter 13: BERT"),
    ("chapter14_gpt", "Chapter 14: GPT"),
    ("chapter15_t5_bart", "Chapter 15: T5 and BART"),
    ("chapter16_efficient_transformers", "Chapter 16: Efficient Transformers"),
    ("chapter17_vision_transformers", "Chapter 17: Vision Transformers"),
    ("chapter18_multimodal_transformers", "Chapter 18: Multimodal Transformers"),
    ("chapter19_long_context", "Chapter 19: Long Context Handling"),
    ("chapter20_pretraining_strategies", "Chapter 20: Pretraining Strategies"),
    ("chapter21_pytorch_implementation", "Chapter 21: PyTorch Implementation"),
    ("chapter22_hardware_optimization", "Chapter 22: Hardware Optimization"),
    ("chapter23_best_practices", "Chapter 23: Best Practices"),
]

def read_latex_file(filepath):
    """Read LaTeX file content"""
    # Handle both relative and absolute paths
    if not filepath.exists():
        # Try relative to project root
        project_root = Path(__file__).parent.parent
        filepath = project_root / filepath
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: File not found: {filepath}")
        return None

def convert_latex_to_html(latex_content):
    """Convert LaTeX content to HTML with preserved math"""
    if not latex_content:
        return ""
    
    html = latex_content
    
    # Remove LaTeX comments
    html = re.sub(r'(?<!\\)%.*$', '', html, flags=re.MULTILINE)
    
    # Convert tables FIRST - before any other conversions
    def convert_table_environment(match):
        """Convert entire table environment including wrapper and tabular"""
        full_content = match.group(0)
        
        # Extract just the tabular content
        tabular_match = re.search(r'\\begin\{tabular\}\{[^}]+\}(.*?)\\end\{tabular\}', full_content, re.DOTALL)
        if not tabular_match:
            return full_content
        
        table_content = tabular_match.group(1)
        
        # Remove all booktabs and table formatting commands with surrounding whitespace
        # These can appear on their own lines or inline
        table_content = re.sub(r'\s*\\toprule\s*', '\n', table_content)
        table_content = re.sub(r'\s*\\midrule\s*', '\n', table_content)
        table_content = re.sub(r'\s*\\bottomrule\s*', '\n', table_content)
        table_content = re.sub(r'\s*\\hline\s*', '\n', table_content)
        
        # Split by \\ for rows
        rows = [r.strip() for r in table_content.split('\\\\') if r.strip()]
        
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
    
    # Match entire table environment
    tables_found = len(re.findall(r'\\begin\{table\}.*?\\end\{table\}', html, flags=re.DOTALL))
    html = re.sub(r'\\begin\{table\}.*?\\end\{table\}', convert_table_environment, html, flags=re.DOTALL)
    tables_after = html.count('<table>')
    
    if tables_found > 0:
        print(f"  → Converted {tables_found} table environments to {tables_after} HTML tables [v2-FIXED]")
    
    # Convert chapters and sections
    html = re.sub(r'\\chapter\*?\{([^}]+)\}', r'<h1>\1</h1>', html)
    html = re.sub(r'\\section\*?\{([^}]+)\}', r'<h2>\1</h2>', html)
    html = re.sub(r'\\subsection\*?\{([^}]+)\}', r'<h3>\1</h3>', html)
    html = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'<h4>\1</h4>', html)
    
    # Convert environments - handle both with and without labels
    html = re.sub(r'\\begin\{definition\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', r'<div class="definition"><strong>Definition:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{definition\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{theorem\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', r'<div class="theorem"><strong>Theorem:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{theorem\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{lemma\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', r'<div class="lemma"><strong>Lemma:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{lemma\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{corollary\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', r'<div class="corollary"><strong>Corollary:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{corollary\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{proposition\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', r'<div class="proposition"><strong>Proposition:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{proposition\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{example\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', r'<div class="example"><strong>Example:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{example\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{exercise\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', r'<div class="exercise"><strong>Exercise:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{exercise\}', r'</div>', html)
    
    # Convert proof environment
    def format_proof(match):
        optional_title = match.group(2) if match.group(2) else ''
        if optional_title:
            return f'<div class="proof"><strong>Proof ({optional_title}):</strong> '
        else:
            return '<div class="proof"><strong>Proof:</strong> '
    
    html = re.sub(r'\\begin\{proof\}(\[([^\]]+)\])?', format_proof, html, flags=re.DOTALL)
    html = re.sub(r'\\end\{proof\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{keypoint\}', r'<div class="keypoint">', html)
    html = re.sub(r'\\end\{keypoint\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{implementation\}', r'<div class="implementation">', html)
    html = re.sub(r'\\end\{implementation\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{caution\}', r'<div class="caution">', html)
    html = re.sub(r'\\end\{caution\}', r'</div>', html)
    
    # Convert itemize and enumerate
    html = re.sub(r'\\begin\{itemize\}', r'<ul>', html)
    html = re.sub(r'\\end\{itemize\}', r'</ul>', html)
    html = re.sub(r'\\begin\{enumerate\}', r'<ol>', html)
    html = re.sub(r'\\end\{enumerate\}', r'</ol>', html)
    html = re.sub(r'\\item\s+', r'<li>', html)
    
    # Convert center environment
    html = re.sub(r'\\begin\{center\}', r'<div style="text-align: center;">', html)
    html = re.sub(r'\\end\{center\}', r'</div>', html)
    
    # Convert standalone tabular environments (not wrapped in table environment)
    def convert_standalone_tabular(match):
        """Convert tabular environments that aren't inside table environments"""
        table_content = match.group(1)
        
        # Remove all booktabs and table formatting commands with surrounding whitespace
        table_content = re.sub(r'\s*\\toprule\s*', '\n', table_content)
        table_content = re.sub(r'\s*\\midrule\s*', '\n', table_content)
        table_content = re.sub(r'\s*\\bottomrule\s*', '\n', table_content)
        table_content = re.sub(r'\s*\\hline\s*', '\n', table_content)
        
        # Split by \\ for rows
        rows = [r.strip() for r in table_content.split('\\\\') if r.strip()]
        
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
    
    # Convert standalone tabular environments
    html = re.sub(r'\\begin\{tabular\}\{[^}]+\}(.*?)\\end\{tabular\}', convert_standalone_tabular, html, flags=re.DOTALL)
    
    # Convert text formatting - handle nested braces properly
    def convert_textbf(match):
        content = match.group(1)
        return f'<strong>{content}</strong>'
    
    def convert_textit(match):
        content = match.group(1)
        return f'<em>{content}</em>'
    
    def convert_texttt(match):
        content = match.group(1)
        return f'<code>{content}</code>'
    
    # Match \textbf{...} with proper brace counting
    def find_and_replace_command(html, command, converter):
        result = []
        i = 0
        pattern = f'\\{command}{{'
        
        while i < len(html):
            pos = html.find(pattern, i)
            if pos == -1:
                result.append(html[i:])
                break
            
            # Add text before the command
            result.append(html[i:pos])
            
            # Find the matching closing brace
            brace_count = 1
            j = pos + len(pattern)
            start = j
            
            while j < len(html) and brace_count > 0:
                if html[j] == '{':
                    brace_count += 1
                elif html[j] == '}':
                    brace_count -= 1
                j += 1
            
            if brace_count == 0:
                content = html[start:j-1]
                result.append(converter(content))
                i = j
            else:
                # Unmatched braces, keep original
                result.append(pattern)
                i = pos + len(pattern)
        
        return ''.join(result)
    
    html = find_and_replace_command(html, 'textbf', lambda c: f'<strong>{c}</strong>')
    html = find_and_replace_command(html, 'textit', lambda c: f'<em>{c}</em>')
    html = find_and_replace_command(html, 'texttt', lambda c: f'<code>{c}</code>')
    
    # Convert equations (preserve LaTeX for MathJax)
    # Display equations - use $$ delimiters which MathJax handles better
    html = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', r'<div class="equation">\n$$\1$$\n</div>', html, flags=re.DOTALL)
    html = re.sub(r'\\begin\{align\}(.*?)\\end\{align\}', r'<div class="equation">\n$$\\begin{align}\1\\end{align}$$\n</div>', html, flags=re.DOTALL)
    html = re.sub(r'\\begin\{align\*\}(.*?)\\end\{align\*\}', r'<div class="equation">\n$$\\begin{align*}\1\\end{align*}$$\n</div>', html, flags=re.DOTALL)
    
    # Convert lstlisting to code blocks
    html = re.sub(r'\\begin\{lstlisting\}.*?\n(.*?)\\end\{lstlisting\}', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Convert algorithm environment
    html = re.sub(r'\\begin\{algorithm\}.*?\\caption\{([^}]+)\}.*?\\label\{[^}]+\}', r'<div class="algorithm"><div class="algorithm-title">Algorithm: \1</div>', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{algorithm\}', r'</div>', html)
    
    # Remove remaining LaTeX commands that don't need conversion
    html = re.sub(r'\\label\{[^}]+\}', '', html)
    html = re.sub(r'\\ref\{[^}]+\}', '[ref]', html)
    html = re.sub(r'\\cite\{[^}]+\}', '[citation]', html)
    html = re.sub(r'\\addcontentsline\{[^}]+\}\{[^}]+\}\{[^}]+\}', '', html)
    
    # Clean up paragraphs - but don't wrap block elements
    # Split by double newlines
    parts = re.split(r'\n\n+', html)
    
    # Only wrap text parts in <p> tags, not block elements
    wrapped_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Check if it's a block element (starts with <h, <div, <ul, <ol, <pre, <table)
        if re.match(r'^\s*<(h[1-6]|div|ul|ol|pre|table|blockquote)', part):
            wrapped_parts.append(part)
        else:
            wrapped_parts.append(f'<p>{part}</p>')
    
    html = '\n\n'.join(wrapped_parts)
    
    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    
    # Fix any remaining nested p tags
    html = re.sub(r'<p>\s*(<h[1-6]>)', r'\1', html)
    html = re.sub(r'(</h[1-6]>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>\s*(<div)', r'\1', html)
    html = re.sub(r'(</div>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>\s*(<ul>|<ol>)', r'\1', html)
    html = re.sub(r'(</ul>|</ol>)\s*</p>', r'\1', html)
    
    return html

def create_chapter_html(chapter_file, chapter_title, prev_chapter=None, next_chapter=None):
    """Create HTML file for a chapter"""
    # Use absolute path from project root
    project_root = Path(__file__).parent.parent
    latex_path = project_root / "chapters" / f"{chapter_file}.tex"
    
    latex_content = read_latex_file(latex_path)
    
    if not latex_content:
        return
    
    html_content = convert_latex_to_html(latex_content)
    
    # Navigation
    nav_html = '<div class="chapter-nav">\n'
    if prev_chapter:
        nav_html += f'  <a href="{prev_chapter[0]}.html">← {prev_chapter[1]}</a>\n'
    else:
        nav_html += '  <span></span>\n'
    
    nav_html += '  <a href="../index.html">📚 Table of Contents</a>\n'
    
    if next_chapter:
        nav_html += f'  <a href="{next_chapter[0]}.html">{next_chapter[1]} →</a>\n'
    else:
        nav_html += '  <span></span>\n'
    nav_html += '</div>\n'
    
    # Full HTML page
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chapter_title} - Deep Learning and Transformers</title>
    <link rel="stylesheet" href="../css/style.css">
    
    <!-- MathJax Configuration (must come before loading MathJax) -->
    <script>
    window.MathJax = {{
        tex: {{
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
            processEscapes: true,
            processEnvironments: true,
            tags: 'ams',
            macros: {{
                R: '{{\\\\mathbb{{R}}}}',
                N: '{{\\\\mathbb{{N}}}}',
                Z: '{{\\\\mathbb{{Z}}}}',
                C: '{{\\\\mathbb{{C}}}}',
                va: '{{\\\\mathbf{{a}}}}',
                vb: '{{\\\\mathbf{{b}}}}',
                vc: '{{\\\\mathbf{{c}}}}',
                vd: '{{\\\\mathbf{{d}}}}',
                ve: '{{\\\\mathbf{{e}}}}',
                vf: '{{\\\\mathbf{{f}}}}',
                vg: '{{\\\\mathbf{{g}}}}',
                vh: '{{\\\\mathbf{{h}}}}',
                vi: '{{\\\\mathbf{{i}}}}',
                vj: '{{\\\\mathbf{{j}}}}',
                vk: '{{\\\\mathbf{{k}}}}',
                vl: '{{\\\\mathbf{{l}}}}',
                vm: '{{\\\\mathbf{{m}}}}',
                vn: '{{\\\\mathbf{{n}}}}',
                vo: '{{\\\\mathbf{{o}}}}',
                vp: '{{\\\\mathbf{{p}}}}',
                vq: '{{\\\\mathbf{{q}}}}',
                vr: '{{\\\\mathbf{{r}}}}',
                vs: '{{\\\\mathbf{{s}}}}',
                vt: '{{\\\\mathbf{{t}}}}',
                vu: '{{\\\\mathbf{{u}}}}',
                vv: '{{\\\\mathbf{{v}}}}',
                vw: '{{\\\\mathbf{{w}}}}',
                vx: '{{\\\\mathbf{{x}}}}',
                vy: '{{\\\\mathbf{{y}}}}',
                vz: '{{\\\\mathbf{{z}}}}',
                mA: '{{\\\\mathbf{{A}}}}',
                mB: '{{\\\\mathbf{{B}}}}',
                mC: '{{\\\\mathbf{{C}}}}',
                mD: '{{\\\\mathbf{{D}}}}',
                mE: '{{\\\\mathbf{{E}}}}',
                mF: '{{\\\\mathbf{{F}}}}',
                mG: '{{\\\\mathbf{{G}}}}',
                mH: '{{\\\\mathbf{{H}}}}',
                mI: '{{\\\\mathbf{{I}}}}',
                mJ: '{{\\\\mathbf{{J}}}}',
                mK: '{{\\\\mathbf{{K}}}}',
                mL: '{{\\\\mathbf{{L}}}}',
                mM: '{{\\\\mathbf{{M}}}}',
                mN: '{{\\\\mathbf{{N}}}}',
                mO: '{{\\\\mathbf{{O}}}}',
                mP: '{{\\\\mathbf{{P}}}}',
                mQ: '{{\\\\mathbf{{Q}}}}',
                mR: '{{\\\\mathbf{{R}}}}',
                mS: '{{\\\\mathbf{{S}}}}',
                mT: '{{\\\\mathbf{{T}}}}',
                mU: '{{\\\\mathbf{{U}}}}',
                mV: '{{\\\\mathbf{{V}}}}',
                mW: '{{\\\\mathbf{{W}}}}',
                mX: '{{\\\\mathbf{{X}}}}',
                mY: '{{\\\\mathbf{{Y}}}}',
                mZ: '{{\\\\mathbf{{Z}}}}',
                transpose: '{{^\\\\top}}',
                norm: ['\\\\left\\\\|#1\\\\right\\\\|', 1],
                abs: ['\\\\left|#1\\\\right|', 1]
            }}
        }},
        startup: {{
            pageReady: () => {{
                console.log('MathJax loaded and ready');
                return MathJax.startup.defaultPageReady();
            }}
        }}
    }};
    </script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <nav>
        <a href="../index.html">🏠 Home</a>
        <a href="preface.html">Preface</a>
        <a href="notation.html">Notation</a>
        <a href="chapter01_linear_algebra.html">Ch 1</a>
        <a href="chapter02_calculus_optimization.html">Ch 2</a>
        <a href="chapter03_probability_information.html">Ch 3</a>
        <a href="chapter04_feedforward_networks.html">Ch 4</a>
        <a href="chapter05_convolutional_networks.html">Ch 5</a>
        <a href="chapter06_recurrent_networks.html">Ch 6</a>
        <a href="chapter07_attention_fundamentals.html">Ch 7</a>
        <a href="chapter08_self_attention.html">Ch 8</a>
        <a href="chapter09_attention_variants.html">Ch 9</a>
        <a href="chapter10_transformer_model.html">Ch 10</a>
        <a href="chapter11_training_transformers.html">Ch 11</a>
        <a href="chapter12_computational_analysis.html">Ch 12</a>
        <a href="chapter13_bert.html">Ch 13</a>
        <a href="chapter14_gpt.html">Ch 14</a>
        <a href="chapter15_t5_bart.html">Ch 15</a>
        <a href="chapter16_efficient_transformers.html">Ch 16</a>
        <a href="chapter17_vision_transformers.html">Ch 17</a>
        <a href="chapter18_multimodal_transformers.html">Ch 18</a>
        <a href="chapter19_long_context.html">Ch 19</a>
        <a href="chapter20_pretraining_strategies.html">Ch 20</a>
        <a href="chapter21_pytorch_implementation.html">Ch 21</a>
        <a href="chapter22_hardware_optimization.html">Ch 22</a>
        <a href="chapter23_best_practices.html">Ch 23</a>
    </nav>

    <main>
        {html_content}
        
        {nav_html}
    </main>

    <footer>
        <p>&copy; 2026 Deep Learning and Transformers Textbook. All rights reserved.</p>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>
"""
    
    # Write HTML file
    output_path = Path(f"output/chapters/{chapter_file}.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Created: {output_path}")

def create_index_html():
    """Create main index page"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deep Learning and Transformers - A Graduate-Level Course</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <header>
        <h1>Deep Learning and Transformers</h1>
        <p style="font-size: 1.2em; text-align: center; color: #666;">
            Theory, Mathematics, and Implementation<br>
            <em>A Graduate-Level Course</em>
        </p>
    </header>

    <main>
        <div class="toc">
            <h2>Table of Contents</h2>
            
            <h3>Front Matter</h3>
            <ul>
                <li><a href="chapters/preface.html">Preface</a></li>
                <li><a href="chapters/notation.html">Notation and Conventions</a></li>
            </ul>

            <h3>Part I: Mathematical Foundations</h3>
            <ul>
                <li><a href="chapters/chapter01_linear_algebra.html">Chapter 1: Linear Algebra for Deep Learning</a></li>
                <li><a href="chapters/chapter02_calculus_optimization.html">Chapter 2: Calculus and Optimization</a></li>
                <li><a href="chapters/chapter03_probability_information.html">Chapter 3: Probability and Information Theory</a></li>
            </ul>

            <h3>Part II: Neural Network Fundamentals</h3>
            <ul>
                <li><a href="chapters/chapter04_feedforward_networks.html">Chapter 4: Feed-Forward Neural Networks</a></li>
                <li><a href="chapters/chapter05_convolutional_networks.html">Chapter 5: Convolutional Neural Networks</a></li>
                <li><a href="chapters/chapter06_recurrent_networks.html">Chapter 6: Recurrent Neural Networks</a></li>
            </ul>

            <h3>Part III: Attention Mechanisms</h3>
            <ul>
                <li><a href="chapters/chapter07_attention_fundamentals.html">Chapter 7: Attention Mechanisms: Fundamentals</a></li>
                <li><a href="chapters/chapter08_self_attention.html">Chapter 8: Self-Attention and Multi-Head Attention</a></li>
                <li><a href="chapters/chapter09_attention_variants.html">Chapter 9: Attention Variants and Mechanisms</a></li>
            </ul>

            <h3>Part IV-VII: Coming Soon</h3>
            <ul>
                <li>Part IV: Transformer Architecture</li>
                <li>Part V: Modern Transformer Variants</li>
                <li>Part VI: Advanced Topics</li>
                <li>Part VII: Practical Implementation</li>
            </ul>
        </div>

        <div style="margin-top: 3em; padding: 2em; background-color: #f8f9fa; border-radius: 5px;">
            <h2>About This Book</h2>
            <p>
                This textbook provides a comprehensive, graduate-level treatment of deep learning and transformer architectures.
                It emphasizes mathematical rigor while maintaining practical relevance, with complete derivations,
                concrete numerical examples, and implementation guidance.
            </p>
            <p>
                <strong>Key Features:</strong>
            </p>
            <ul>
                <li>Complete mathematical derivations with geometric intuition</li>
                <li>Explicit dimension tracking for all operations</li>
                <li>Concrete numerical examples from real models (BERT, GPT, etc.)</li>
                <li>Implementation notes and code examples</li>
                <li>Progressive complexity building from foundations</li>
            </ul>
        </div>
    </main>

    <footer>
        <p>&copy; 2026 Deep Learning and Transformers Textbook. All rights reserved.</p>
        <p>
            <a href="https://github.com/PietKonijn007/deep-learning-transformers-textbook">View on GitHub</a>
        </p>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
"""
    
    output_path = Path("output/index.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Created: {output_path}")

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
        
        # Handle \For{...}{ - check for this pattern anywhere in the line
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
        
        # Regular line - skip if it's just a leftover LaTeX command
        if line and not line.startswith('\\'):
            result.append(f'<div class="algorithm-line">{line}</div>')
    
    # Close any remaining indent blocks
    while indent_level > 0:
        result.append('</div>')
        indent_level -= 1
    
    return '\n'.join(result)

def fix_algorithms():
    """Fix algorithm formatting in all generated HTML files."""
    output_dir = Path("output/chapters")
    
    for filepath in sorted(output_dir.glob("chapter*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find all algorithm blocks
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
            print(f"  ✓ Fixed algorithms in {filepath.name}")

def main():
    """Main conversion function"""
    print("Converting LaTeX textbook to HTML...")
    
    # Create output directories
    Path("output/chapters").mkdir(parents=True, exist_ok=True)
    Path("output/css").mkdir(parents=True, exist_ok=True)
    Path("output/js").mkdir(parents=True, exist_ok=True)
    
    # Copy CSS and JS - use absolute paths from project root
    import shutil
    project_root = Path(__file__).parent.parent
    
    # Copy the correct CSS file
    source_css = project_root / "docs" / "css" / "style.css"
    dest_css = Path("output/css/style.css")
    
    if source_css.exists():
        shutil.copy(source_css, dest_css)
        print(f"✓ Copied CSS from {source_css}")
    else:
        print(f"⚠ Warning: CSS file not found at {source_css}")
    
    # Copy JS if it exists
    source_js = project_root / "docs" / "js" / "main.js"
    dest_js = Path("output/js/main.js")
    
    if source_js.exists():
        shutil.copy(source_js, dest_js)
        print(f"✓ Copied JS from {source_js}")
    else:
        # Create a minimal main.js if it doesn't exist
        dest_js.write_text("// Main JavaScript file\nconsole.log('Deep Learning Textbook loaded');")
        print(f"✓ Created minimal JS file")
    
    # Convert each chapter
    for i, (chapter_file, chapter_title) in enumerate(CHAPTERS):
        prev_chapter = CHAPTERS[i-1] if i > 0 else None
        next_chapter = CHAPTERS[i+1] if i < len(CHAPTERS)-1 else None
        create_chapter_html(chapter_file, chapter_title, prev_chapter, next_chapter)
    
    # Create index
    create_index_html()
    
    # Fix algorithm formatting
    print("\nFixing algorithm formatting...")
    fix_algorithms()
    
    print("\n✅ Conversion complete!")
    print("📂 Output directory: output/")
    print("🌐 Open output/index.html in your browser")

if __name__ == "__main__":
    main()
