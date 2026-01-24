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
]

def read_latex_file(filepath):
    """Read LaTeX file content"""
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
    
    # Convert chapters and sections
    html = re.sub(r'\\chapter\*?\{([^}]+)\}', r'<h1>\1</h1>', html)
    html = re.sub(r'\\section\*?\{([^}]+)\}', r'<h2>\1</h2>', html)
    html = re.sub(r'\\subsection\*?\{([^}]+)\}', r'<h3>\1</h3>', html)
    html = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'<h4>\1</h4>', html)
    
    # Convert environments
    html = re.sub(r'\\begin\{definition\}.*?\\label\{[^}]+\}', r'<div class="definition"><strong>Definition:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{definition\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{theorem\}.*?\\label\{[^}]+\}', r'<div class="theorem"><strong>Theorem:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{theorem\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{example\}.*?\\label\{[^}]+\}', r'<div class="example"><strong>Example:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{example\}', r'</div>', html)
    
    html = re.sub(r'\\begin\{exercise\}.*?\\label\{[^}]+\}', r'<div class="exercise"><strong>Exercise:</strong> ', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{exercise\}', r'</div>', html)
    
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
    
    # Convert text formatting
    html = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', html)
    html = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', html)
    html = re.sub(r'\\texttt\{([^}]+)\}', r'<code>\1</code>', html)
    
    # Convert equations (preserve LaTeX for MathJax)
    # Display equations
    html = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', r'<div class="equation">\n\\[\1\\]\n</div>', html, flags=re.DOTALL)
    html = re.sub(r'\\begin\{align\}(.*?)\\end\{align\}', r'<div class="equation">\n\\begin{align}\1\\end{align}\n</div>', html, flags=re.DOTALL)
    html = re.sub(r'\\begin\{align\*\}(.*?)\\end\{align\*\}', r'<div class="equation">\n\\begin{align*}\1\\end{align*}\n</div>', html, flags=re.DOTALL)
    
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
    
    # Clean up paragraphs
    html = re.sub(r'\n\n+', '</p>\n<p>', html)
    html = '<p>' + html + '</p>'
    
    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    
    return html

def create_chapter_html(chapter_file, chapter_title, prev_chapter=None, next_chapter=None):
    """Create HTML file for a chapter"""
    latex_path = Path(f"../chapters/{chapter_file}.tex")
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

def main():
    """Main conversion function"""
    print("Converting LaTeX textbook to HTML...")
    
    # Create output directories
    Path("output/chapters").mkdir(parents=True, exist_ok=True)
    Path("output/css").mkdir(parents=True, exist_ok=True)
    Path("output/js").mkdir(parents=True, exist_ok=True)
    
    # Copy CSS and JS
    import shutil
    shutil.copy("css/style.css", "output/css/style.css")
    shutil.copy("js/main.js", "output/js/main.js")
    print("Copied CSS and JS files")
    
    # Convert each chapter
    for i, (chapter_file, chapter_title) in enumerate(CHAPTERS):
        prev_chapter = CHAPTERS[i-1] if i > 0 else None
        next_chapter = CHAPTERS[i+1] if i < len(CHAPTERS)-1 else None
        create_chapter_html(chapter_file, chapter_title, prev_chapter, next_chapter)
    
    # Create index
    create_index_html()
    
    print("\n✅ Conversion complete!")
    print("📂 Output directory: output/")
    print("🌐 Open output/index.html in your browser")

if __name__ == "__main__":
    main()
