#!/bin/bash

# Script to compile each chapter individually to identify LaTeX errors

chapters=(
    "chapter01_linear_algebra"
    "chapter02_calculus_optimization"
    "chapter03_probability_information"
    "chapter04_feedforward_networks"
    "chapter05_convolutional_networks"
    "chapter06_recurrent_networks"
    "chapter07_attention_fundamentals"
    "chapter08_self_attention"
    "chapter09_attention_variants"
    "chapter10_transformer_model"
    "chapter11_training_transformers"
    "chapter12_computational_analysis"
    "chapter13_bert"
    "chapter14_gpt"
    "chapter15_t5_bart"
    "chapter16_efficient_transformers"
    "chapter17_vision_transformers"
    "chapter18_multimodal_transformers"
    "chapter19_long_context"
    "chapter20_pretraining_strategies"
    "chapter21_pytorch_implementation"
    "chapter22_hardware_optimization"
    "chapter23_best_practices"
)

echo "Starting individual chapter compilation..."
echo "=========================================="

for chapter in "${chapters[@]}"; do
    echo ""
    echo "Compiling $chapter..."
    
    # Create test file
    cat > "test_${chapter}.tex" << 'PREAMBLE'
\documentclass[11pt]{book}
\usepackage{amsmath, amssymb, amsthm, mathtools}
\usepackage{bm}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{array}
\usepackage{xcolor}
\definecolor{deepblue}{RGB}{0,51,102}
\definecolor{darkgreen}{RGB}{0,100,0}
\definecolor{darkred}{RGB}{139,0,0}
\usepackage[ruled,vlined,linesnumbered]{algorithm2e}
\usepackage{listings}
\lstset{
    language=Python,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{deepblue},
    commentstyle=\color{darkgreen},
    stringstyle=\color{darkred},
    showstringspaces=false,
    breaklines=true,
    frame=single,
    numbers=left,
    numberstyle=\tiny\color{gray}
}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=deepblue,citecolor=darkgreen,urlcolor=deepblue}
\usepackage[capitalise,noabbrev]{cleveref}
\usepackage[margin=1in]{geometry}
\usepackage{microtype}
\usepackage{framed}

\theoremstyle{definition}
\newtheorem{definition}{Definition}
\newtheorem{example}{Example}
\newtheorem{exercise}{Exercise}
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{remark}
\newtheorem{remark}{Remark}
\newtheorem{note}{Note}

\makeatletter
\def\thm@space@setup{\thm@preskip=\parskip \thm@postskip=0pt}
\makeatother

\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\vx}{\mathbf{x}}
\newcommand{\vy}{\mathbf{y}}
\newcommand{\vz}{\mathbf{z}}
\newcommand{\vh}{\mathbf{h}}
\newcommand{\vw}{\mathbf{w}}
\newcommand{\vb}{\mathbf{b}}
\newcommand{\vq}{\mathbf{q}}
\newcommand{\vk}{\mathbf{k}}
\newcommand{\vv}{\mathbf{v}}
\newcommand{\va}{\mathbf{a}}
\newcommand{\vc}{\mathbf{c}}
\newcommand{\vf}{\mathbf{f}}
\newcommand{\vi}{\mathbf{i}}
\newcommand{\vo}{\mathbf{o}}
\newcommand{\vr}{\mathbf{r}}
\newcommand{\vt}{\mathbf{t}}
\newcommand{\mA}{\mathbf{A}}
\newcommand{\mB}{\mathbf{B}}
\newcommand{\mC}{\mathbf{C}}
\newcommand{\mW}{\mathbf{W}}
\newcommand{\mX}{\mathbf{X}}
\newcommand{\mY}{\mathbf{Y}}
\newcommand{\mQ}{\mathbf{Q}}
\newcommand{\mK}{\mathbf{K}}
\newcommand{\mV}{\mathbf{V}}
\newcommand{\mH}{\mathbf{H}}
\newcommand{\mI}{\mathbf{I}}
\newcommand{\mU}{\mathbf{U}}
\newcommand{\mJ}{\mathbf{J}}
\newcommand{\mE}{\mathbf{E}}
\newcommand{\mM}{\mathbf{M}}
\newcommand{\mZ}{\mathbf{Z}}
\newcommand{\mT}{\mathbf{T}}
\newcommand{\mR}{\mathbf{R}}
\newcommand{\mF}{\mathbf{F}}
\newcommand{\mS}{\mathbf{S}}
\newcommand{\transpose}{^\top}
\newcommand{\norm}[1]{\left\|#1\right\|}
\newcommand{\abs}[1]{\left|#1\right|}
\newcommand{\dimof}[1]{\text{dim}(#1)}

\definecolor{keypoint-bg}{RGB}{227, 242, 253}
\definecolor{impl-bg}{RGB}{232, 245, 233}
\definecolor{caution-bg}{RGB}{255, 235, 238}

\newenvironment{keypoint}{%
  \def\FrameCommand{\fboxsep=8pt\colorbox{keypoint-bg}}%
  \MakeFramed{\advance\hsize-\width\FrameRestore}%
  \noindent\textbf{Key Point:}\par\vspace{4pt}%
}{\endMakeFramed}

\newenvironment{implementation}{%
  \def\FrameCommand{\fboxsep=8pt\colorbox{impl-bg}}%
  \MakeFramed{\advance\hsize-\width\FrameRestore}%
  \noindent\textbf{Implementation:}\par\vspace{4pt}%
}{\endMakeFramed}

\newenvironment{caution}{%
  \def\FrameCommand{\fboxsep=8pt\colorbox{caution-bg}}%
  \MakeFramed{\advance\hsize-\width\FrameRestore}%
  \noindent\textbf{Caution:}\par\vspace{4pt}%
}{\endMakeFramed}

\begin{document}
PREAMBLE
    
    echo "\input{chapters/${chapter}.tex}" >> "test_${chapter}.tex"
    echo "\end{document}" >> "test_${chapter}.tex"
    
    # Compile with xelatex
    xelatex -interaction=nonstopmode "test_${chapter}.tex" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✓ $chapter compiled successfully"
    else
        echo "✗ $chapter has errors - check test_${chapter}.log"
    fi
done

echo ""
echo "=========================================="
echo "Compilation complete. Check individual .log files for errors."
