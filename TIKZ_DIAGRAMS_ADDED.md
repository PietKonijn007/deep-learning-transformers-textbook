# TikZ Computational Graph Diagrams Added

## Status: ✅ COMPLETE - All Overlap Issues Resolved

I've added professional TikZ diagrams showing computational graphs and information flow to chapters 4-18. These diagrams visualize how neurons connect and how information flows through the networks, making abstract concepts concrete and educational.

**Update (Jan 31, 2026):** All text overlap issues have been resolved by removing inline text labels from TikZ environments. Diagrams now display cleanly with all explanations provided in comprehensive captions. PDF compiles successfully: 757 pages, 2.93 MB.

---

## Chapters 4-10: Core Neural Network Architectures

### Chapter 4: Feed-Forward Networks
**Diagram**: MLP Fully-Connected Graph (Figure \ref{fig:mlp_architecture})
- Shows all connections between input (3 nodes) → hidden (4 nodes) → output (2 nodes)
- Highlights fully-connected nature: every input connects to every hidden node
- Demonstrates weight sharing and layer-wise computation

### Chapter 5: Convolutional Networks
**Diagram**: Convolutional Receptive Field (Figure \ref{fig:conv_receptive_field})
- Shows local 3×3 connectivity vs fully-connected
- Highlights weight sharing across spatial positions
- Demonstrates parameter efficiency of convolutions

### Chapter 6: Recurrent Networks
**Diagram 1**: RNN Unrolled Through Time (Figure \ref{fig:rnn_unrolled})
- Shows sequential dependencies: h₀ → h₁ → h₂ → h₃
- Highlights why RNNs cannot parallelize
- Demonstrates weight sharing across time steps

**Diagram 2**: LSTM Gate Structure (Figure \ref{fig:lstm_gates})
- Shows all 4 gates: forget, input, candidate, output
- Highlights cell state "highway" for gradient flow
- Demonstrates element-wise operations (⊙, +)

### Chapter 7: Attention Fundamentals
**Diagram**: Scaled Dot-Product Attention (Figure \ref{fig:scaled_dot_product_attention})
- Shows computational flow: Q, K, V → QK^T → softmax → attention weights → output
- Highlights matrix dimensions at each stage
- Demonstrates how queries attend to keys

### Chapter 8: Self-Attention
**Diagram 1**: Self-Attention Connectivity (Figure \ref{fig:self_attention_connectivity})
- Shows all-to-all connections: every input connects to every output
- Contrasts with RNN sequential connections
- Demonstrates why self-attention can parallelize

**Diagram 2**: Multi-Head Attention (Figure \ref{fig:multi_head_attention})
- Shows parallel computation across heads
- Demonstrates independent projections per head
- Highlights concatenation and output projection

### Chapter 9: Attention Variants
**Diagram**: Causal Masking (Figure \ref{fig:causal_masking})
- Shows triangular connectivity pattern
- Contrasts bidirectional vs causal attention
- Demonstrates position-dependent visibility

### Chapter 10: Transformer Model
**Diagram**: Transformer Encoder Layer (Figure \ref{fig:transformer_encoder_layer})
- Shows complete layer: attention → add & norm → FFN → add & norm
- Highlights residual connections as curved arrows
- Demonstrates dimension preservation throughout

---

## Chapters 11-16: Training, Analysis, and Architectures

### Chapter 11: Training Transformers
**Diagram**: Gradient Flow Through Residual Connections (Figure \ref{fig:residual_gradient_flow})
- Shows forward pass: x → F(x) → add → y
- Shows backward pass: gradients flow through both direct path and F(x)
- Highlights the "gradient highway" that prevents vanishing gradients
- Blue arrows show direct residual path, red dashed arrows show gradient flow

**Key insight**: The direct gradient path bypasses F(x), ensuring gradients can flow through many layers without vanishing.

### Chapter 12: Computational Analysis
**Diagram**: Attention vs FFN Complexity (Figure \ref{fig:attention_vs_ffn_complexity})
- Shows computational flow for self-attention: X → QKV → QK^T → AV → Output
- Shows computational flow for FFN: X → W₁ → GELU → W₂ → Output
- Highlights complexity: Attention O(8nd² + 4n²d) vs FFN O(16nd²)
- Color-coded: green (matrix mult), red (quadratic bottleneck), orange (element-wise)

**Key insight**: For typical sequences (n < 2d), FFN requires ~2× the FLOPs of attention. For long sequences (n > 2d), attention dominates.

### Chapter 13: BERT
**Diagram**: BERT Bidirectional Attention (Figure \ref{fig:bert_bidirectional_attention})
- Shows all-to-all bidirectional connections between tokens
- Demonstrates that each output h_i depends on entire input sequence
- Blue double-headed arrows show bidirectional information flow
- Contrasts with GPT's unidirectional attention

**Key insight**: Bidirectional attention enables rich contextual representations ideal for understanding tasks.

### Chapter 14: GPT
**Diagram**: GPT Causal Attention (Figure \ref{fig:gpt_causal_attention})
- Shows triangular connectivity pattern: each token only sees previous tokens
- Red arrows show unidirectional causal masking
- Demonstrates progressive visibility: h₁ sees x₁, h₂ sees x₁,x₂, etc.
- Contrasts with BERT's bidirectional attention

**Key insight**: Causal masking enables autoregressive generation while preventing information leakage from future positions.

### Chapter 15: T5 and BART
**Diagram**: T5 Encoder-Decoder Architecture (Figure \ref{fig:t5_encoder_decoder})
- Shows encoder with bidirectional attention (blue)
- Shows decoder with causal attention (red)
- Shows cross-attention from decoder to encoder (green dashed)
- Demonstrates how encoder-decoder combines BERT's understanding with GPT's generation

**Key insight**: Cross-attention allows decoder to attend to all encoder outputs, enabling sequence-to-sequence transformations.

### Chapter 16: Efficient Transformers
**Diagram 1**: Longformer Attention Pattern (Figure \ref{fig:longformer_attention})
- Shows local sliding window connections (blue)
- Shows global token connections (red)
- Yellow highlights global tokens (e.g., CLS)
- Demonstrates O(n) complexity with local + global pattern

**Key insight**: Combines local context (window) with long-range information flow (global tokens) for efficient long-document processing.

**Diagram 2**: BigBird Attention Pattern (Figure \ref{fig:bigbird_attention})
- Shows three connection types for a single query token:
  - Local window (blue)
  - Random connections (green dashed)
  - Global tokens (red)
- Orange highlights the query token
- Demonstrates hybrid sparse pattern

**Key insight**: Random connections provide long-range connectivity while maintaining O(n) complexity.

---

## Chapters 17-18: Vision and Multimodal Transformers

### Chapter 17: Vision Transformers
**Diagram**: ViT Patch Embedding Process (Figure \ref{fig:vit_patch_embedding})
- Shows image divided into patches (4×4 grid representation)
- Shows linear projection of flattened patches
- Shows CLS token prepended to sequence
- Shows position embeddings added
- Demonstrates complete pipeline: image → patches → embeddings → transformer

**Key insight**: Converts 2D images to 1D sequences by dividing into patches, enabling standard transformer processing. 224×224 image becomes 196 tokens (much shorter than 50,176 pixels).

### Chapter 18: Multimodal Transformers
**Diagram**: Multimodal Fusion Strategies (Figure \ref{fig:multimodal_fusion_strategies})
- Shows three fusion approaches side-by-side:
  - **Early fusion**: Unified encoder, O((N+M)²) complexity
  - **Late fusion**: Separate encoders, O(N² + M²) complexity
  - **Cross-modal attention**: Separate encoders with cross-attention, O(N² + M² + NM) complexity
- Blue nodes represent vision tokens, red nodes represent text tokens
- Green dashed arrows show cross-attention connections

**Key insight**: Cross-modal attention balances computational efficiency with rich cross-modal interactions, avoiding the quadratic cost of early fusion while enabling better alignment than late fusion.

---

## Diagram Features

### Visual Elements:
- **Circles**: Neurons/tokens/hidden states
- **Rectangles**: Operations, layers, transformations
- **Arrows**: 
  - Solid thick: Forward data flow
  - Blue: Input/bidirectional connections
  - Red: Recurrent/causal/important paths
  - Green: Cross-attention/operations
  - Dashed: Gradients/random connections
- **Colors**:
  - Blue: Bidirectional/input
  - Red: Causal/recurrent/gradients
  - Green: Operations/cross-attention
  - Yellow: Global/special tokens
  - Orange: Focus/query tokens

### Educational Value:
1. **Connectivity patterns**: Shows which neurons/tokens connect to which
2. **Sequential vs parallel**: RNN sequential vs attention parallel
3. **Bidirectional vs causal**: BERT vs GPT attention patterns
4. **Weight sharing**: Same weights across time/space
5. **Gradient flow**: Residual highways, cell state paths
6. **Dimension tracking**: Tensor shapes at each stage
7. **Complexity visualization**: Where computation happens
8. **Sparse patterns**: Efficient attention mechanisms

---

## Complete Chapter Coverage

**Chapters with diagrams**: 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18

**Total diagrams added**: 18 TikZ figures

**Architecture types covered**:
- Feed-forward networks (MLP)
- Convolutional networks (CNN)
- Recurrent networks (RNN, LSTM)
- Attention mechanisms (scaled dot-product, self-attention, multi-head)
- Transformers (encoder, decoder, encoder-decoder)
- Efficient transformers (sparse attention patterns)
- Vision transformers (patch embedding)
- Multimodal transformers (fusion strategies)
- Training dynamics (gradient flow, residual connections)
- Computational analysis (complexity visualization)

---

## Compilation

These diagrams use the TikZ package which should already be included in your LaTeX preamble. Compile with:

```bash
pdflatex main_pro.tex
```

Or use your existing compilation script:

```bash
./compile_chapters.sh
```

The diagrams are publication-quality vector graphics that scale perfectly in PDF output.

---

## Diagram Style Consistency

All diagrams follow consistent styling:
- **Font**: \small for nodes, \footnotesize for labels
- **Arrow style**: thick with stealth tips
- **Node sizes**: Consistent across diagrams
- **Color scheme**: Blue (bidirectional), Red (causal/gradients), Green (operations), Yellow (global)
- **Spacing**: Adequate white space for readability
- **Captions**: Detailed explanations of key insights

This ensures visual consistency across all chapters and makes the book feel cohesive.
