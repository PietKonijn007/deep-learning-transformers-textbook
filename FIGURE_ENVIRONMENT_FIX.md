# Figure Environment HTML Conversion Fix

## Issue

LaTeX `\begin{figure}` and `\end{figure}` commands were appearing as raw text in the HTML output instead of being properly converted to HTML `<figure>` elements.

## Solution

Added proper figure environment handling to the `convert_latex_to_html()` function in `html-build/convert_to_html.py`.

### Implementation Details

1. **Figure Environment Conversion**
   - Detects `\begin{figure}[positioning]...\end{figure}` blocks
   - Extracts caption text (handling nested braces correctly)
   - Removes LaTeX-specific commands (`\centering`, `\label`)
   - Converts to HTML `<figure>` with `<figcaption>`

2. **Nested Brace Handling**
   - Implemented proper brace counting algorithm
   - Correctly extracts captions containing `\textbf{}`, math, etc.
   - Prevents caption text from being truncated

3. **Block Element Treatment**
   - Added `<figure>` to block element list
   - Prevents wrapping in `<p>` tags
   - Cleans up any nested `<p><figure>` structures

### Code Changes

```python
def convert_figure(match):
    """Convert LaTeX figure environment to HTML"""
    content = match.group(1)
    
    # Extract caption with proper brace counting
    caption = ''
    caption_start = content.find('\\caption{')
    if caption_start != -1:
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
    
    # Remove LaTeX commands
    if caption:
        content = content.replace(f'\\caption{{{caption}}}', '')
    content = re.sub(r'\\label\{[^}]+\}', '', content)
    content = re.sub(r'\\centering\s*', '', content)
    content = content.strip()
    
    # Build HTML
    if caption:
        return f'<figure>\n{content}\n<figcaption>{caption}</figcaption>\n</figure>'
    else:
        return f'<figure>\n{content}\n</figure>'
```

### CSS Improvements

Enhanced figure and caption styling:

```css
figure {
    margin: 2em 0;
    text-align: center;
}

figcaption {
    font-style: italic;
    color: #666;
    margin-top: 1em;
    padding: 0 1em;
    text-align: justify;
    font-size: 0.95em;
    line-height: 1.6;
}

figure .tikz-diagram {
    margin: 0 auto;
}
```

## Before

```html
\begin{figure}[h] \centering

<div class="tikz-diagram"><img src="diagrams/..." /></div>

\caption{Multi-layer perceptron (MLP) computational graph...}

\end{figure}
```

## After

```html
<figure>
<div class="tikz-diagram"><img src="diagrams/..." /></div>
<figcaption>Multi-layer perceptron (MLP) computational graph showing fully-connected layers. Each neuron in the hidden layer receives input from <strong>all</strong> neurons in the input layer (12 connections total), and each output neuron receives input from all hidden neurons (8 connections). The red path highlights one example: $x_1 \to h_2 \to y_1$. This dense connectivity enables MLPs to learn complex non-linear functions.</figcaption>
</figure>
```

## Benefits

1. **Semantic HTML**: Proper use of `<figure>` and `<figcaption>` elements
2. **Accessibility**: Screen readers can properly identify figures and captions
3. **Styling**: CSS can target figures and captions independently
4. **Clean Output**: No raw LaTeX commands in HTML
5. **Responsive**: Figures adapt to different screen sizes

## Files Modified

- `html-build/convert_to_html.py` - Added figure conversion logic
- `css/style.css` - Enhanced figure and caption styling
- Copied to all output directories (chapters/, nodejs-version/public/, docs/)

## Testing

Verified with Chapter 4 (Feed-Forward Networks) which contains TikZ diagrams in figure environments. All figures now render correctly with proper captions.

## Status

✅ **Complete** - Figure environments are now properly converted to semantic HTML with styled captions.

---

*Last Updated: January 31, 2026*
