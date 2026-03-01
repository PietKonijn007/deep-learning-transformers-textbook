#!/usr/bin/env python3
"""
Build all PDFs for the Deep Learning & Transformers textbook.
  1. main_pro.pdf          — full book (standard)
  2. main_pro_memoir.pdf   — full book (memoir class)
  3. Per-chapter PDFs      — chapters/DeepLearningTech-XX-Title.pdf
"""

import os
import subprocess
import shutil
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(SCRIPT_DIR, ".chapter_build")
CHAPTERS_DIR = os.path.join(SCRIPT_DIR, "chapters")
PREAMBLE_FILE = os.path.join(SCRIPT_DIR, "chapter_preamble.tex")

os.makedirs(BUILD_DIR, exist_ok=True)


def build_main_pdf(tex_name):
    """Compile a main .tex file (twice for TOC/refs). Returns True on success."""
    tex_path = os.path.join(SCRIPT_DIR, tex_name)
    pdf_name = tex_name.replace(".tex", ".pdf")
    if not os.path.exists(tex_path):
        print(f"  SKIP: {tex_name} not found")
        return False

    print(f"Building: {pdf_name} ... ", end="", flush=True)

    # Remove old PDF so we can detect fresh creation
    old_pdf = os.path.join(SCRIPT_DIR, pdf_name)
    if os.path.exists(old_pdf):
        os.remove(old_pdf)

    for _ in range(2):
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_path],
            cwd=SCRIPT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    if os.path.exists(old_pdf):
        size_mb = os.path.getsize(old_pdf) / (1024 * 1024)
        print(f"OK ({size_mb:.1f} MB)")
        return True
    else:
        print(f"FAILED (check {tex_name.replace('.tex', '.log')})")
        return False

CHAPTERS = [
    ("chapter01_linear_algebra",         "01-Linear-Algebra"),
    ("chapter02_calculus_optimization",   "02-Calculus-and-Optimization"),
    ("chapter03_probability_information", "03-Probability-and-Information"),
    ("chapter04_feedforward_networks",    "04-Feedforward-Networks"),
    ("chapter05_convolutional_networks",  "05-Convolutional-Networks"),
    ("chapter06_recurrent_networks",      "06-Recurrent-Networks"),
    ("chapter07_attention_fundamentals",  "07-Attention-Fundamentals"),
    ("chapter08_self_attention",          "08-Self-Attention"),
    ("chapter09_attention_variants",      "09-Attention-Variants"),
    ("chapter10_transformer_model",       "10-The-Transformer-Model"),
    ("chapter11_training_transformers",   "11-Training-Transformers"),
    ("chapter12_computational_analysis",  "12-Computational-Analysis"),
    ("chapter13_bert",                    "13-BERT"),
    ("chapter14_gpt",                     "14-GPT"),
    ("chapter15_t5_bart",                 "15-T5-and-BART"),
    ("chapter16_efficient_transformers",  "16-Efficient-Transformers"),
    ("chapter17_vision_transformers",     "17-Vision-Transformers"),
    ("chapter18_multimodal_transformers", "18-Multimodal-Transformers"),
    ("chapter19_long_context",            "19-Long-Context"),
    ("chapter20_pretraining_strategies",  "20-Pretraining-Strategies"),
    ("chapter21_pytorch_implementation",  "21-PyTorch-Implementation"),
    ("chapter22_hardware_optimization",   "22-From-PyTorch-to-Accelerator-Silicon"),
    ("chapter23_best_practices",          "23-Best-Practices"),
    ("chapter24_domain_specific_models",  "24-Domain-Specific-Models"),
    ("chapter25_enterprise_nlp",          "25-Enterprise-NLP"),
    ("chapter26_code_language",           "26-Code-and-Language"),
    ("chapter27_video_visual",            "27-Video-and-Visual"),
    ("chapter28_knowledge_graphs",        "28-Knowledge-Graphs"),
    ("chapter29_recommendations",         "29-Recommendations"),
    ("chapter30_healthcare",              "30-Healthcare"),
    ("chapter31_finance",                 "31-Finance"),
    ("chapter32_legal",                   "32-Legal"),
    ("chapter33_observability",           "33-Observability"),
    ("chapter34_dsl_agents",              "34-DSL-and-Agents"),
]

# ── Step 1: Build full-book PDFs ─────────────────────────────────────────
print("=" * 64)
print("  FULL BOOK PDFs")
print("=" * 64)

main_ok = build_main_pdf("main_pro.tex")
memoir_ok = build_main_pdf("main_pro_memoir.tex")

# ── Step 2: Build per-chapter PDFs ──────────────────────────────────────
print()
print("=" * 64)
print("  INDIVIDUAL CHAPTER PDFs")
print("=" * 64)

# Read the shared preamble
with open(PREAMBLE_FILE, "r") as f:
    preamble = f.read()

total = 0
success = 0
fail = 0

for basename, title in CHAPTERS:
    tex_path = os.path.join(CHAPTERS_DIR, f"{basename}.tex")
    if not os.path.exists(tex_path):
        print(f"  SKIP: {basename}.tex not found")
        continue

    chap_num = title.split("-")[0]           # e.g. "01"
    chap_counter = int(chap_num) - 1
    pretty_title = title.split("-", 1)[1].replace("-", " ")
    pdf_name = f"DeepLearningTech-{title}.pdf"
    total += 1

    print(f"Building: {pdf_name} ... ", end="", flush=True)

    # Create standalone wrapper .tex
    wrapper_path = os.path.join(BUILD_DIR, f"standalone_{basename}.tex")
    doc_body = f"""
\\title{{Deep Learning and Transformers\\\\\\large Chapter {chap_num}: {pretty_title}}}
\\author{{[Author Names]}}
\\date{{2026}}

\\begin{{document}}
\\maketitle
\\setcounter{{chapter}}{{{chap_counter}}}
\\input{{chapters/{basename}}}
\\end{{document}}
"""
    with open(wrapper_path, "w") as f:
        f.write(preamble + "\n" + doc_body)

    # Compile twice (for cross-references)
    # pdflatex often returns non-zero on warnings, so we check for the PDF instead
    for _ in range(2):
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode",
             f"-output-directory={BUILD_DIR}", wrapper_path],
            cwd=SCRIPT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    built_pdf = os.path.join(BUILD_DIR, f"standalone_{basename}.pdf")
    if os.path.exists(built_pdf):
        shutil.copy2(built_pdf, os.path.join(CHAPTERS_DIR, pdf_name))
        print("OK")
        success += 1
    else:
        print(f"FAILED (see {BUILD_DIR}/standalone_{basename}.log)")
        fail += 1

print(f"\nDone: {success}/{total} chapter PDFs succeeded, {fail} failed")
print()
print("=" * 64)
print("  SUMMARY")
print("=" * 64)
print(f"  main_pro.pdf:         {'OK' if main_ok else 'FAILED'}")
print(f"  main_pro_memoir.pdf:  {'OK' if memoir_ok else 'FAILED'}")
print(f"  Chapter PDFs:         {success}/{total}")
print(f"  Output:               {CHAPTERS_DIR}/")
print(f"  Clean build files:    rm -rf {BUILD_DIR}")
print("=" * 64)
