#!/usr/bin/env python3
"""
Convert LaTeX textbook to HTML with MathJax support
"""

import os
import re
import sys
import subprocess
import tempfile
import hashlib
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
    ("chapter22_hardware_optimization", "Chapter 22: From PyTorch to Accelerator Silicon"),
    ("chapter23_best_practices", "Chapter 23: Best Practices"),
    ("chapter24_domain_specific_models", "Chapter 24: Domain-Specific Models"),
    ("chapter25_enterprise_nlp", "Chapter 25: Enterprise NLP"),
    ("chapter26_code_language", "Chapter 26: Code and Language Models"),
    ("chapter27_video_visual", "Chapter 27: Video and Visual Understanding"),
    ("chapter28_knowledge_graphs", "Chapter 28: Knowledge Graphs and Reasoning"),
    ("chapter29_recommendations", "Chapter 29: Recommendation Systems"),
    ("chapter30_healthcare", "Chapter 30: Healthcare Applications"),
    ("chapter31_finance", "Chapter 31: Financial Applications"),
    ("chapter32_legal", "Chapter 32: Legal and Compliance Applications"),
    ("chapter33_observability", "Chapter 33: Observability and Monitoring"),
    ("chapter34_dsl_agents", "Chapter 34: DSL and Agent Systems"),
]

def extract_tikz_diagrams(latex_content, chapter_name):
    """Extract TikZ diagrams from LaTeX content and return list of (tikz_code, hash) tuples"""
    diagrams = []
    
    # Find all tikzpicture environments
    pattern = r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}'
    matches = re.finditer(pattern, latex_content, re.DOTALL)
    
    for match in matches:
        tikz_code = match.group(0)
        # Create a hash for the diagram to use as filename
        diagram_hash = hashlib.md5(tikz_code.encode()).hexdigest()[:12]
        diagrams.append((tikz_code, diagram_hash))
    
    return diagrams

def convert_tikz_to_svg(tikz_code, output_path, chapter_name, diagram_hash):
    """Convert a single TikZ diagram to SVG using pdflatex and pdf2svg or ImageMagick"""
    
    # Check if pdflatex is available
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"   ⚠ pdflatex not found - skipping TikZ conversion")
        print(f"      Install MacTeX: brew install --cask mactex")
        return False
    
    # Check for pdf2svg or ImageMagick convert
    has_pdf2svg = False
    has_imagemagick = False
    
    try:
        subprocess.run(['pdf2svg'], capture_output=True)
        has_pdf2svg = True
    except FileNotFoundError:
        pass
    
    try:
        result = subprocess.run(['convert', '--version'], capture_output=True)
        if b'ImageMagick' in result.stdout:
            has_imagemagick = True
    except FileNotFoundError:
        pass
    
    if not has_pdf2svg and not has_imagemagick:
        print(f"   ⚠ Neither pdf2svg nor ImageMagick found - skipping TikZ conversion")
        print(f"      Install with: brew install pdf2svg  OR  brew install imagemagick")
        return False
    
    # Create a standalone LaTeX document with the TikZ code
    standalone_doc = r'''\documentclass[tikz,border=2pt]{standalone}
\usepackage{tikz}
\usepackage{amsmath,amssymb,amsthm,bm}
\usetikzlibrary{arrows,arrows.meta,positioning,shapes,calc}

% Custom macros from main_pro.tex
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\C}{\mathbb{C}}

% Vector commands
\newcommand{\va}{\mathbf{a}}
\newcommand{\vb}{\mathbf{b}}
\newcommand{\vc}{\mathbf{c}}
\newcommand{\vd}{\mathbf{d}}
\newcommand{\ve}{\mathbf{e}}
\newcommand{\vf}{\mathbf{f}}
\newcommand{\vg}{\mathbf{g}}
\newcommand{\vh}{\mathbf{h}}
\newcommand{\vi}{\mathbf{i}}
\newcommand{\vj}{\mathbf{j}}
\newcommand{\vk}{\mathbf{k}}
\newcommand{\vl}{\mathbf{l}}
\newcommand{\vm}{\mathbf{m}}
\newcommand{\vn}{\mathbf{n}}
\newcommand{\vo}{\mathbf{o}}
\newcommand{\vp}{\mathbf{p}}
\newcommand{\vq}{\mathbf{q}}
\newcommand{\vr}{\mathbf{r}}
\newcommand{\vs}{\mathbf{s}}
\newcommand{\vt}{\mathbf{t}}
\newcommand{\vu}{\mathbf{u}}
\newcommand{\vv}{\mathbf{v}}
\newcommand{\vw}{\mathbf{w}}
\newcommand{\vx}{\mathbf{x}}
\newcommand{\vy}{\mathbf{y}}
\newcommand{\vz}{\mathbf{z}}

% Matrix commands
\newcommand{\mA}{\mathbf{A}}
\newcommand{\mB}{\mathbf{B}}
\newcommand{\mC}{\mathbf{C}}
\newcommand{\mD}{\mathbf{D}}
\newcommand{\mE}{\mathbf{E}}
\newcommand{\mF}{\mathbf{F}}
\newcommand{\mG}{\mathbf{G}}
\newcommand{\mH}{\mathbf{H}}
\newcommand{\mI}{\mathbf{I}}
\newcommand{\mJ}{\mathbf{J}}
\newcommand{\mK}{\mathbf{K}}
\newcommand{\mL}{\mathbf{L}}
\newcommand{\mM}{\mathbf{M}}
\newcommand{\mN}{\mathbf{N}}
\newcommand{\mO}{\mathbf{O}}
\newcommand{\mP}{\mathbf{P}}
\newcommand{\mQ}{\mathbf{Q}}
\newcommand{\mR}{\mathbf{R}}
\newcommand{\mS}{\mathbf{S}}
\newcommand{\mT}{\mathbf{T}}
\newcommand{\mU}{\mathbf{U}}
\newcommand{\mV}{\mathbf{V}}
\newcommand{\mW}{\mathbf{W}}
\newcommand{\mX}{\mathbf{X}}
\newcommand{\mY}{\mathbf{Y}}
\newcommand{\mZ}{\mathbf{Z}}

\begin{document}
''' + tikz_code + r'''
\end{document}
'''
    
    # Create temporary directory for compilation
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tex_file = tmpdir / f"{diagram_hash}.tex"
        pdf_file = tmpdir / f"{diagram_hash}.pdf"
        
        # Write the standalone document
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(standalone_doc)
        
        try:
            # Compile to PDF
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex_file.name],
                cwd=tmpdir,
                capture_output=True,
                timeout=30
            )
            
            if result.returncode != 0 or not pdf_file.exists():
                print(f"   ⚠ Failed to compile TikZ diagram {diagram_hash}")
                # Print error output for debugging
                if result.stderr:
                    error_lines = result.stderr.decode('utf-8', errors='ignore').split('\n')
                    # Print last few lines of error
                    for line in error_lines[-5:]:
                        if line.strip():
                            print(f"      {line.strip()}")
                return False
            
            # Convert PDF to SVG using available tool
            if has_pdf2svg:
                result = subprocess.run(
                    ['pdf2svg', pdf_file.name, output_path.name],
                    cwd=tmpdir,
                    capture_output=True,
                    timeout=30
                )
            else:  # Use ImageMagick
                result = subprocess.run(
                    ['convert', '-density', '300', pdf_file.name, output_path.name],
                    cwd=tmpdir,
                    capture_output=True,
                    timeout=30
                )
            
            if result.returncode != 0:
                print(f"   ⚠ Failed to convert PDF to SVG for {diagram_hash}")
                return False
            
            # Move the SVG to the output directory
            svg_file = tmpdir / output_path.name
            if svg_file.exists():
                svg_file.rename(output_path)
                return True
            else:
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ⚠ Timeout while processing TikZ diagram {diagram_hash}")
            return False
        except Exception as e:
            print(f"   ⚠ Error processing TikZ diagram {diagram_hash}: {e}")
            return False

def process_tikz_diagrams(latex_content, chapter_name, output_dirs):
    """Extract and convert all TikZ diagrams in the content, return modified content"""
    
    # Extract all TikZ diagrams
    diagrams = extract_tikz_diagrams(latex_content, chapter_name)
    
    if not diagrams:
        return latex_content
    
    print(f"   → Found {len(diagrams)} TikZ diagram(s)")
    
    # Create diagrams directory in each output location
    for output_dir in output_dirs:
        diagrams_dir = output_dir / "diagrams"
        diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert each diagram
    converted_count = 0
    for tikz_code, diagram_hash in diagrams:
        svg_filename = f"{chapter_name}_{diagram_hash}.svg"
        
        # Convert to SVG (use first output dir for conversion)
        primary_output = output_dirs[0] / "diagrams" / svg_filename
        
        if convert_tikz_to_svg(tikz_code, primary_output, chapter_name, diagram_hash):
            converted_count += 1
            
            # Copy to other output directories
            for output_dir in output_dirs[1:]:
                dest = output_dir / "diagrams" / svg_filename
                if primary_output.exists():
                    import shutil
                    shutil.copy2(primary_output, dest)
            
            # Replace TikZ code with SVG reference in the LaTeX content
            # Wrap in figure environment if not already
            svg_html = f'<div class="tikz-diagram"><img src="../diagrams/{svg_filename}" alt="TikZ Diagram" /></div>'
            
            # Replace the tikzpicture with a placeholder that will be converted to HTML
            placeholder = f"%%%TIKZ_SVG:{svg_filename}%%%"
            latex_content = latex_content.replace(tikz_code, placeholder)
    
    if converted_count > 0:
        print(f"   ✓ Converted {converted_count}/{len(diagrams)} TikZ diagram(s) to SVG")
    
    return latex_content

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
    
    # Convert TikZ SVG placeholders to HTML img tags
    html = re.sub(
        r'%%%TIKZ_SVG:([^%]+)%%%',
        r'<div class="tikz-diagram"><img src="../diagrams/\1" alt="TikZ Diagram" /></div>',
        html
    )
    
    # Convert figure environments
    # Handle figure with caption and label
    def convert_figure(match):
        """Convert LaTeX figure environment to HTML"""
        content = match.group(1)
        
        # Extract caption if present - handle nested braces
        caption = ''
        caption_start = content.find('\\caption{')
        if caption_start != -1:
            # Find matching closing brace
            brace_count = 0
            i = caption_start + len('\\caption{')
            start_pos = i
            while i < len(content):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    if brace_count == 0:
                        caption = content[start_pos:i]
                        break
                    brace_count -= 1
                i += 1
        
        # Remove caption and label commands from content
        if caption:
            content = content.replace(f'\\caption{{{caption}}}', '')
        content = re.sub(r'\\label\{[^}]+\}', '', content)
        
        # Remove \centering command
        content = re.sub(r'\\centering\s*', '', content)
        
        # Clean up extra whitespace
        content = content.strip()
        
        # Build HTML figure
        if caption:
            return f'<figure>\n{content}\n<figcaption>{caption}</figcaption>\n</figure>'
        else:
            return f'<figure>\n{content}\n</figure>'
    
    # Match figure environments (with optional positioning like [h], [htbp], etc.)
    html = re.sub(
        r'\\begin\{figure\}(?:\[[^\]]*\])?\s*(.*?)\\end\{figure\}',
        convert_figure,
        html,
        flags=re.DOTALL
    )
    
    # Build a label-to-number mapping for exercises
    label_map = {}
    exercise_counter = 0
    
    # Find all exercise labels and assign numbers
    exercise_pattern = r'\\begin\{exercise\}.*?\\label\{([^}]+)\}'
    for match in re.finditer(exercise_pattern, html, re.DOTALL):
        exercise_counter += 1
        label = match.group(1)
        label_map[label] = exercise_counter
    
    # Remove LaTeX comments
    html = re.sub(r'(?<!\\)%.*$', '', html, flags=re.MULTILINE)
    
    # Convert tables FIRST - before any other conversions
    def convert_table_environment(match):
        """Convert entire table environment including wrapper and tabular"""
        full_content = match.group(0)
        
        # Extract tabular content - need to handle nested braces in column spec
        # Find \begin{tabular}{ and then match balanced braces
        start_match = re.search(r'\\begin\{tabular\}\{', full_content)
        if not start_match:
            return full_content
        
        # Find the matching closing brace for column spec
        pos = start_match.end()
        brace_count = 1
        while pos < len(full_content) and brace_count > 0:
            if full_content[pos] == '{':
                brace_count += 1
            elif full_content[pos] == '}':
                brace_count -= 1
            pos += 1
        
        if brace_count != 0:
            return full_content  # Unbalanced braces
        
        # Now extract content between column spec end and \end{tabular}
        content_start = pos
        end_match = re.search(r'\\end\{tabular\}', full_content[content_start:])
        if not end_match:
            return full_content
        
        table_content = full_content[content_start:content_start + end_match.start()]
        
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
    # Handle \chapter[short]{long} format - use the long title
    html = re.sub(r'\\chapter\*?\[([^\]]+)\]\{([^}]+)\}', r'<h1>\2</h1>', html)
    # Handle \chapter{title} format
    html = re.sub(r'\\chapter\*?\{([^}]+)\}', r'<h1>\1</h1>', html)
    
    # Handle sections with optional short titles
    html = re.sub(r'\\section\*?\[([^\]]+)\]\{([^}]+)\}', r'<h2>\2</h2>', html)
    html = re.sub(r'\\section\*?\{([^}]+)\}', r'<h2>\1</h2>', html)
    
    html = re.sub(r'\\subsection\*?\[([^\]]+)\]\{([^}]+)\}', r'<h3>\2</h3>', html)
    html = re.sub(r'\\subsection\*?\{([^}]+)\}', r'<h3>\1</h3>', html)
    
    html = re.sub(r'\\subsubsection\*?\[([^\]]+)\]\{([^}]+)\}', r'<h4>\2</h4>', html)
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
    
    # Convert exercise environment with numbering
    exercise_num = 0
    def format_exercise(match):
        nonlocal exercise_num
        exercise_num += 1
        return f'<div class="exercise" id="exercise-{exercise_num}"><strong>Exercise {exercise_num}:</strong> '
    
    html = re.sub(r'\\begin\{exercise\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', format_exercise, html, flags=re.DOTALL)
    html = re.sub(r'\\end\{exercise\}', r'</div>', html)
    
    # Convert solution environment with reference to exercise number
    def format_solution(match):
        optional_ref = match.group(2) if match.group(2) else ''
        
        # Try to extract exercise reference
        ref_match = re.search(r'\\ref\{([^}]+)\}', optional_ref)
        if ref_match:
            label = ref_match.group(1)
            if label in label_map:
                exercise_num = label_map[label]
                return f'<div class="solution"><strong>Solution to Exercise {exercise_num}:</strong> '
        
        # Fallback if no reference found
        return '<div class="solution"><strong>Solution:</strong> '
    
    html = re.sub(r'\\begin\{solution\}(\[([^\]]+)\])?\s*(\\label\{[^}]+\})?', format_solution, html, flags=re.DOTALL)
    html = re.sub(r'\\end\{solution\}', r'</div>', html)
    
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
        full_content = match.group(0)
        
        # Find \begin{tabular}{ and then match balanced braces
        start_match = re.search(r'\\begin\{tabular\}\{', full_content)
        if not start_match:
            return full_content
        
        # Find the matching closing brace for column spec
        pos = start_match.end()
        brace_count = 1
        while pos < len(full_content) and brace_count > 0:
            if full_content[pos] == '{':
                brace_count += 1
            elif full_content[pos] == '}':
                brace_count -= 1
            pos += 1
        
        if brace_count != 0:
            return full_content  # Unbalanced braces
        
        # Now extract content between column spec end and \end{tabular}
        content_start = pos
        end_match = re.search(r'\\end\{tabular\}', full_content[content_start:])
        if not end_match:
            return full_content
        
        table_content = full_content[content_start:content_start + end_match.start()]
        
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
    html = re.sub(r'\\begin\{tabular\}\{[^}]+\}.*?\\end\{tabular\}', convert_standalone_tabular, html, flags=re.DOTALL)
    
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
    
    # Convert verbatim to code blocks
    html = re.sub(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Convert algorithm environment
    html = re.sub(r'\\begin\{algorithm\}.*?\\caption\{([^}]+)\}.*?\\label\{[^}]+\}', r'<div class="algorithm"><div class="algorithm-title">Algorithm: \1</div>', html, flags=re.DOTALL)
    html = re.sub(r'\\end\{algorithm\}', r'</div>', html)
    
    # Remove remaining LaTeX commands that don't need conversion
    html = re.sub(r'\\label\{[^}]+\}', '', html)
    html = re.sub(r'\\ref\{[^}]+\}', '[ref]', html)
    html = re.sub(r'\\cite\{[^}]+\}', '[citation]', html)
    html = re.sub(r'\\addcontentsline\{[^}]+\}\{[^}]+\}\{[^}]+\}', '', html)
    
    # Protect pre/code blocks from paragraph processing by replacing newlines with placeholders
    pre_blocks = []
    def save_pre_block(match):
        pre_blocks.append(match.group(0))
        return f'___PRE_BLOCK_{len(pre_blocks)-1}___'
    
    html = re.sub(r'<pre><code>.*?</code></pre>', save_pre_block, html, flags=re.DOTALL)
    
    # Clean up paragraphs - but don't wrap block elements
    # Split by double newlines
    parts = re.split(r'\n\n+', html)
    
    # Only wrap text parts in <p> tags, not block elements
    wrapped_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Check if it's a block element (starts with <h, <div, <ul, <ol, <pre, <table, <figure) or a placeholder
        if re.match(r'^\s*<(h[1-6]|div|ul|ol|pre|table|blockquote|figure)', part) or '___PRE_BLOCK_' in part:
            wrapped_parts.append(part)
        else:
            wrapped_parts.append(f'<p>{part}</p>')
    
    html = '\n\n'.join(wrapped_parts)
    
    # Restore pre/code blocks
    for i, block in enumerate(pre_blocks):
        html = html.replace(f'___PRE_BLOCK_{i}___', block)
    
    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    
    # Fix any remaining nested p tags
    html = re.sub(r'<p>\s*(<h[1-6]>)', r'\1', html)
    html = re.sub(r'(</h[1-6]>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>\s*(<div)', r'\1', html)
    html = re.sub(r'(</div>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>\s*(<ul>|<ol>)', r'\1', html)
    html = re.sub(r'(</ul>|</ol>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>\s*(<figure)', r'\1', html)
    html = re.sub(r'(</figure>)\s*</p>', r'\1', html)
    
    return html

def create_chapter_html(chapter_file, chapter_title, prev_chapter=None, next_chapter=None, output_dirs=None):
    """Create HTML file for a chapter"""
    if output_dirs is None:
        output_dirs = [Path("output")]
    
    # Use absolute path from project root
    project_root = Path(__file__).parent.parent
    latex_path = project_root / "chapters" / f"{chapter_file}.tex"
    
    latex_content = read_latex_file(latex_path)
    
    if not latex_content:
        return
    
    # Process TikZ diagrams before converting to HTML
    latex_content = process_tikz_diagrams(latex_content, chapter_file, output_dirs)
    
    html_content = convert_latex_to_html(latex_content)
    
    # Navigation
    nav_html = '<div class="chapter-nav">\n'
    if prev_chapter:
        nav_html += f'  <a href="{prev_chapter[0]}.html">← {prev_chapter[1]}</a>\n'
    else:
        nav_html += '  <span></span>\n'
    
    nav_html += '  <a href="../../deeptech.html">📚 Table of Contents</a>\n'
    
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
    <link rel="stylesheet" href="../../styles.css">
    
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
        <a href="../../deeptech.html">🏠 Home</a>
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
        <a href="chapter24_domain_specific_models.html">Ch 24</a>
        <a href="chapter25_enterprise_nlp.html">Ch 25</a>
        <a href="chapter26_code_language.html">Ch 26</a>
        <a href="chapter27_video_visual.html">Ch 27</a>
        <a href="chapter28_knowledge_graphs.html">Ch 28</a>
        <a href="chapter29_recommendations.html">Ch 29</a>
        <a href="chapter30_healthcare.html">Ch 30</a>
        <a href="chapter31_finance.html">Ch 31</a>
        <a href="chapter32_legal.html">Ch 32</a>
        <a href="chapter33_observability.html">Ch 33</a>
        <a href="chapter34_dsl_agents.html">Ch 34</a>
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
    
    # Write HTML file to all output directories
    for output_dir in output_dirs:
        output_path = output_dir / f"{chapter_file}.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
    
    print(f"   ✓ {chapter_file}.html")

def create_index_html(output_dirs=None):
    """Create main index page"""
    if output_dirs is None:
        output_dirs = [Path("output")]
    
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
    
    for base_dir in output_dirs:
        output_path = base_dir / "index.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    print(f"Created: index.html")

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

def fix_algorithms_in_dir(output_dir):
    """Fix algorithm formatting in all generated HTML files in a directory."""
    output_dir = Path(output_dir)
    
    if not output_dir.exists():
        return
    
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

def update_app_js_chapters(chapters_list, output_paths):
    """Update app.js files with the current chapter list"""
    
    # Generate JavaScript chapter array
    js_chapters = []
    for chapter_id, chapter_title in chapters_list:
        # Determine part based on chapter content
        if chapter_id == 'preface':
            part = 'Front Matter'
        elif chapter_id == 'notation':
            part = 'Front Matter'
        elif chapter_id.startswith('chapter01') or chapter_id.startswith('chapter02') or chapter_id.startswith('chapter03'):
            part = 'Part I: Mathematical Foundations'
        elif chapter_id.startswith('chapter04') or chapter_id.startswith('chapter05') or chapter_id.startswith('chapter06'):
            part = 'Part II: Neural Network Fundamentals'
        elif chapter_id.startswith('chapter07') or chapter_id.startswith('chapter08') or chapter_id.startswith('chapter09'):
            part = 'Part III: Attention Mechanisms'
        elif chapter_id.startswith('chapter10') or chapter_id.startswith('chapter11') or chapter_id.startswith('chapter12'):
            part = 'Part IV: Transformer Architecture'
        elif chapter_id.startswith('chapter13') or chapter_id.startswith('chapter14') or chapter_id.startswith('chapter15') or chapter_id.startswith('chapter16'):
            part = 'Part V: Modern Transformer Variants'
        elif chapter_id.startswith('chapter17') or chapter_id.startswith('chapter18') or chapter_id.startswith('chapter19') or chapter_id.startswith('chapter20'):
            part = 'Part VI: Advanced Topics'
        elif chapter_id.startswith('chapter21') or chapter_id.startswith('chapter22') or chapter_id.startswith('chapter23'):
            part = 'Part VII: Practical Implementation'
        elif chapter_id.startswith('chapter24') or chapter_id.startswith('chapter25') or chapter_id.startswith('chapter26') or chapter_id.startswith('chapter27') or chapter_id.startswith('chapter28') or chapter_id.startswith('chapter29'):
            part = 'Part VIII: Domain Applications'
        elif chapter_id.startswith('chapter30') or chapter_id.startswith('chapter31') or chapter_id.startswith('chapter32'):
            part = 'Part IX: Industry Applications'
        elif chapter_id.startswith('chapter33') or chapter_id.startswith('chapter34'):
            part = 'Part X: Production Systems'
        else:
            # For new chapters beyond 34, assign to a new part
            chapter_num = int(chapter_id.split('_')[0].replace('chapter', ''))
            if chapter_num >= 35:
                part = 'Part XI: Advanced Topics'
            else:
                part = 'Uncategorized'
        
        js_chapters.append(f"            {{ id: '{chapter_id}', title: '{chapter_title}', part: '{part}' }}")
    
    chapters_js = ',\n'.join(js_chapters)
    
    # Update each app.js file
    for app_js_path in output_paths:
        if not app_js_path.exists():
            print(f"   ⚠ Skipping {app_js_path} (file not found)")
            continue
        
        with open(app_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the chapters array
        pattern = r'(state\.chapters = \[)\s*\{[^}]+\}[^]]*(\];)'
        replacement = f'\\1\n{chapters_js}\n        \\2'
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(app_js_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"   ✓ Updated {app_js_path.relative_to(Path.cwd().parent if 'html-build' in str(Path.cwd()) else Path.cwd())}")
        else:
            print(f"   ⚠ No changes needed in {app_js_path.name}")

def update_server_js_chapters(chapters_list, server_js_path):
    """Update server.js /api/chapters endpoint with the current chapter list"""
    
    if not server_js_path.exists():
        print(f"   ⚠ Skipping {server_js_path} (file not found)")
        return
    
    # Generate JavaScript chapter array (same as app.js)
    js_chapters = []
    for chapter_id, chapter_title in chapters_list:
        # Use same part logic as update_app_js_chapters
        if chapter_id == 'preface':
            part = 'Front Matter'
        elif chapter_id == 'notation':
            part = 'Front Matter'
        elif chapter_id.startswith('chapter01') or chapter_id.startswith('chapter02') or chapter_id.startswith('chapter03'):
            part = 'Part I: Mathematical Foundations'
        elif chapter_id.startswith('chapter04') or chapter_id.startswith('chapter05') or chapter_id.startswith('chapter06'):
            part = 'Part II: Neural Network Fundamentals'
        elif chapter_id.startswith('chapter07') or chapter_id.startswith('chapter08') or chapter_id.startswith('chapter09'):
            part = 'Part III: Attention Mechanisms'
        elif chapter_id.startswith('chapter10') or chapter_id.startswith('chapter11') or chapter_id.startswith('chapter12'):
            part = 'Part IV: Transformer Architecture'
        elif chapter_id.startswith('chapter13') or chapter_id.startswith('chapter14') or chapter_id.startswith('chapter15') or chapter_id.startswith('chapter16'):
            part = 'Part V: Modern Transformer Variants'
        elif chapter_id.startswith('chapter17') or chapter_id.startswith('chapter18') or chapter_id.startswith('chapter19') or chapter_id.startswith('chapter20'):
            part = 'Part VI: Advanced Topics'
        elif chapter_id.startswith('chapter21') or chapter_id.startswith('chapter22') or chapter_id.startswith('chapter23'):
            part = 'Part VII: Practical Implementation'
        elif chapter_id.startswith('chapter24') or chapter_id.startswith('chapter25') or chapter_id.startswith('chapter26') or chapter_id.startswith('chapter27') or chapter_id.startswith('chapter28') or chapter_id.startswith('chapter29'):
            part = 'Part VIII: Domain Applications'
        elif chapter_id.startswith('chapter30') or chapter_id.startswith('chapter31') or chapter_id.startswith('chapter32'):
            part = 'Part IX: Industry Applications'
        elif chapter_id.startswith('chapter33') or chapter_id.startswith('chapter34'):
            part = 'Part X: Production Systems'
        else:
            chapter_num = int(chapter_id.split('_')[0].replace('chapter', ''))
            if chapter_num >= 35:
                part = 'Part XI: Advanced Topics'
            else:
                part = 'Uncategorized'
        
        js_chapters.append(f"    {{ id: '{chapter_id}', title: '{chapter_title}', part: '{part}' }}")
    
    chapters_js = ',\n'.join(js_chapters)
    
    with open(server_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the chapters array in the API endpoint
    pattern = r"(const chapters = \[)\s*\{[^}]+\}[^]]*(\];)"
    replacement = f'\\1\n{chapters_js}\n  \\2'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(server_js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"   ✓ Updated {server_js_path.relative_to(Path.cwd().parent if 'html-build' in str(Path.cwd()) else Path.cwd())}")
    else:
        print(f"   ⚠ No changes needed in {server_js_path.name}")

def main():
    """Main conversion function"""
    print("=" * 70)
    print("Converting LaTeX textbook chapters to HTML")
    print("=" * 70)
    
    # Get project root (parent of html-build)
    project_root = Path(__file__).parent.parent
    
    # Define all output directories
    output_dirs = [
        project_root / "chapters",                    # Root chapters (deployed to Vercel)
        project_root / "nodejs-version" / "public" / "chapters" / "deeptech",  # Node.js version - deep tech book
        project_root / "docs" / "chapters",           # GitHub Pages
    ]
    
    print(f"\n📂 Output directories:")
    for output_dir in output_dirs:
        print(f"   • {output_dir.relative_to(project_root)}")
    
    # Create all output directories
    for output_dir in output_dirs:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📝 Converting {len(CHAPTERS)} chapters...")
    
    # Convert each chapter to all output directories
    for i, (chapter_file, chapter_title) in enumerate(CHAPTERS):
        prev_chapter = CHAPTERS[i-1] if i > 0 else None
        next_chapter = CHAPTERS[i+1] if i < len(CHAPTERS)-1 else None
        create_chapter_html(chapter_file, chapter_title, prev_chapter, next_chapter, output_dirs)
    
    # Fix algorithm formatting in all directories
    print("\n🔧 Fixing algorithm formatting...")
    for output_dir in output_dirs:
        fix_algorithms_in_dir(output_dir)
    
    # Copy TEX files to docs for reference
    print("\n📄 Copying TEX source files to docs...")
    docs_chapters = project_root / "docs" / "chapters"
    chapters_source = project_root / "chapters"
    
    import shutil
    for tex_file in chapters_source.glob("*.tex"):
        dest = docs_chapters / tex_file.name
        shutil.copy2(tex_file, dest)
    print(f"   ✓ Copied {len(list(chapters_source.glob('*.tex')))} TEX files")
    
    # Update app.js files with chapter list
    print("\n🔄 Updating app.js files with chapter list...")
    app_js_paths = [
        project_root / "nodejs-version" / "public" / "app.js",
        project_root / "app.js",  # Root app.js for Vercel deployment
    ]
    update_app_js_chapters(CHAPTERS, app_js_paths)
    
    # Update server.js with chapter list
    print("\n🔄 Updating server.js with chapter list...")
    server_js_path = project_root / "nodejs-version" / "server.js"
    update_server_js_chapters(CHAPTERS, server_js_path)
    
    print("\n" + "=" * 70)
    print("✅ Conversion complete!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   • Chapters converted: {len(CHAPTERS)}")
    print(f"   • Output locations: {len(output_dirs)}")
    print(f"   • App.js files updated: {len(app_js_paths)}")
    print(f"   • Server.js updated: 1")
    print(f"\n🚀 Deployment ready:")
    print(f"   • Root chapters/ → Vercel deployment")
    print(f"   • Root app.js → Vercel deployment (UPDATED)")
    print(f"   • nodejs-version/public/chapters/ → Node.js development")
    print(f"   • nodejs-version/public/app.js → Node.js development (UPDATED)")
    print(f"   • nodejs-version/server.js → API endpoint (UPDATED)")
    print(f"   • docs/chapters/ → GitHub Pages")
    print(f"\n💡 Next steps:")
    print(f"   1. Review generated HTML files")
    print(f"   2. Test locally: python3 -m http.server 8000")
    print(f"   3. Commit: git add chapters/ app.js nodejs-version/ docs/")
    print(f"   4. Push: git push")
    print()

if __name__ == "__main__":
    main()
