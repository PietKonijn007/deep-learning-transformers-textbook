#!/bin/bash

# Build HTML version of the Deep Learning textbook
# This script converts LaTeX to HTML with MathJax support

set -e

echo "Building HTML version of Deep Learning and Transformers textbook..."

# Create output directories
mkdir -p output/chapters
mkdir -p output/css
mkdir -p output/js

# Copy source files to build directory
echo "Copying source files..."
cp -r ../chapters .
cp ../main.tex .
cp ../references.bib .

# Use pandoc to convert each chapter
echo "Converting chapters to HTML..."

chapters=(
    "chapters/preface.tex"
    "chapters/notation.tex"
    "chapters/chapter01_linear_algebra.tex"
    "chapters/chapter02_calculus_optimization.tex"
    "chapters/chapter03_probability_information.tex"
    "chapters/chapter04_feedforward_networks.tex"
    "chapters/chapter05_convolutional_networks.tex"
    "chapters/chapter06_recurrent_networks.tex"
    "chapters/chapter07_attention_fundamentals.tex"
    "chapters/chapter08_self_attention.tex"
    "chapters/chapter09_attention_variants.tex"
)

for chapter in "${chapters[@]}"; do
    if [ -f "$chapter" ]; then
        basename=$(basename "$chapter" .tex)
        echo "Converting $basename..."
        pandoc "$chapter" \
            -f latex \
            -t html5 \
            --mathjax \
            --standalone \
            --css="../css/style.css" \
            -o "output/chapters/${basename}.html"
    fi
done

# Generate index page
echo "Generating index page..."
python3 generate_index.py

# Copy CSS and JS
echo "Copying assets..."
cp css/style.css output/css/
cp js/main.js output/js/

echo "Build complete! Open output/index.html in your browser."
