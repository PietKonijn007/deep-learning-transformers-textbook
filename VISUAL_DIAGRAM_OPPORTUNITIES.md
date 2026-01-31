# Computational Graph Diagram Opportunities for Neural Network Layers

## Executive Summary

After analyzing chapters 4-10, I've identified **significant opportunities** to add **computational graph diagrams** (using TikZ) that show:
1. **Forward pass graphs**: Which neurons connect to which, showing data flow with arrows
2. **Backward pass graphs**: Gradient flow paths, showing which forward activations are needed
3. **Node-level detail**: What each neuron computes (weighted sum, activation, etc.)

These visual graphs would greatly enhance educational value by making abstract matrix operations concrete and showing the actual network topology.

---

## Chapter 4: Feed-Forward Networks

### Current State
- Has mathematical formulas for forward pass: `z^(ℓ) = W^(ℓ)h^(ℓ-1) + b^(ℓ)` and `h^(ℓ) = σ(z^(ℓ))`
- Discusses activation functions (ReLU, GELU) with formulas
- Has MNIST example with dimensions but **no computational graph showing neuron connections**

### **RECOMMENDED GRAPH 1: 3-Layer MLP Computational Graph (Forward)**

TikZ diagram showing:
```
Input Layer (3 nodes)  →  Hidden Layer (4 nodes)  →  Output Layer (2 nodes)

     x₁ ─────┬─────────→ h₁⁽¹⁾ ─────┬─────→ y₁
             │    w₁₁    ↓           │  w₁₁
     x₂ ─────┼─────────→ h₂⁽¹⁾ ─────┼─────→ y₂
             │           ↓           │
     x₃ ─────┴─────────→ h₃⁽¹⁾ ─────┘
                         ↓
                        h₄⁽¹⁾

Each hidden node shows:
  • Weighted sum: z = Σwᵢxᵢ + b
  • Activation: h = ReLU(z)
  
Each arrow labeled with weight value
```

**Key features to show:**
- All connections from input layer to hidden layer (fully connected)
- All connections from hidden layer to output layer
- Each neuron as a circle with two operations: Σ (sum) and σ (activation)
- Weights on edges
- Highlight one path: x₁ → h₁⁽¹⁾ → y₁ with actual computation

### **RECOMMENDED GRAPH 2: Backpropagation Graph (Same Network)**

TikZ diagram showing gradient flow in **reverse**:
```
     x₁ ←─────┬─────────← h₁⁽¹⁾ ←─────┬─────← y₁ ← ∂L/∂y₁
     ↑        │  ∂L/∂w₁₁  ↑            │
     x₂ ←─────┼─────────← h₂⁽¹⁾ ←─────┼─────← y₂ ← ∂L/∂y₂
     ↑        │           ↑            │
     x₃ ←─────┴─────────← h₃⁽¹⁾ ←─────┘
                          ↑
                         h₄⁽¹⁾

Gradient flow shown with dashed arrows
Each node shows what must be stored from forward pass
```

**Key features:**
- Gradients flow backward (right to left)
- Show which forward values are needed at each node
- Highlight that h⁽¹⁾ values must be stored for computing ∂L/∂W⁽²⁾
- Show that x values must be stored for computing ∂L/∂W⁽¹⁾
- Color code: forward values (blue), gradients (red)

**Location**: Section 4.2 (Multi-Layer Perceptrons)

---

## Chapter 5: Convolutional Networks

### Current State
- Has convolution formula: `(X ★ K)ᵢⱼ = Σ Σ Xᵢ₊ₘ,ⱼ₊ₙ · Kₘ,ₙ`
- Example shows 3×3 convolution but **no graph showing receptive field connections**
- Discusses FLOPs but not the actual computation topology

### **RECOMMENDED GRAPH 3: Convolutional Layer Receptive Field Graph**

TikZ diagram showing how one output neuron connects to input:
```
Input Feature Map (5×5):        Output Feature Map (3×3):
┌─────────────────────┐         ┌─────────────┐
│ x₁₁ x₁₂ x₁₃ x₁₄ x₁₅│         │ y₁₁ y₁₂ y₁₃│
│ x₂₁ x₂₂ x₂₃ x₂₄ x₂₅│         │ y₂₁ y₂₂ y₂₃│
│ x₃₁ x₃₂ x₃₃ x₃₄ x₃₅│         │ y₃₁ y₃₂ y₃₃│
│ x₄₁ x₄₂ x₄₃ x₄₄ x₄₅│         └─────────────┘
│ x₅₁ x₅₂ x₅₃ x₅₄ x₅₅│
└─────────────────────┘

Highlight receptive field for y₂₂:
  x₂₂, x₂₃, x₂₄
  x₃₂, x₃₃, x₃₄  ──→ [3×3 kernel] ──→ y₂₂
  x₄₂, x₄₃, x₄₄

Show 9 arrows from these input positions to y₂₂
Each arrow labeled with kernel weight (w₁₁, w₁₂, etc.)
```

**Key features:**
- Show that each output neuron connects to a LOCAL patch of input (not fully connected)
- Show weight sharing: same 9 weights used for all output positions
- Show overlapping receptive fields for adjacent outputs
- Contrast with fully-connected layer (would have 25 connections per output)

### **RECOMMENDED GRAPH 4: Multi-Channel Convolution Graph**

Show how RGB input (3 channels) produces one output:
```
Input (3 channels):              Output (1 channel):
Red channel (3×3)    ┐
Green channel (3×3)  ├──→ [3 kernels] ──→ Sum ──→ y₁₁
Blue channel (3×3)   ┘

Each channel has its own 3×3 kernel
All 27 connections (9 per channel) feed into single output neuron
```

**Location**: Section 5.1 (Convolution Operation) and Section 5.2 (Multi-Channel Convolutions)

---

## Chapter 6: Recurrent Networks

### Current State
- Has RNN formula: `hₜ = tanh(Wₕₕhₜ₋₁ + Wₓₕxₜ + bₕ)`
- LSTM has gate equations but **no graph showing temporal connections**
- Discusses vanishing gradients mathematically but not visually

### **RECOMMENDED GRAPH 5: RNN Unrolled Computational Graph**

TikZ diagram showing RNN unrolled through time:
```
Time:    t=0         t=1         t=2         t=3
         
Input:              x₁          x₂          x₃
                    ↓           ↓           ↓
Hidden:  h₀ ─────→ h₁ ─────→  h₂ ─────→  h₃
         │         │           │           │
         │         ↓           ↓           ↓
Output:            y₁          y₂          y₃

Each hₜ node shows:
  • Input from xₜ (vertical arrow)
  • Recurrent connection from hₜ₋₁ (horizontal arrow)
  • Both feed into: hₜ = tanh(Wₕₕhₜ₋₁ + Wₓₕxₜ + b)
  
Key insight: SAME weights Wₕₕ and Wₓₕ used at every time step!
```

**Key features:**
- Show temporal dependencies clearly (h₀ → h₁ → h₂ → h₃)
- Highlight weight sharing across time
- Show that each hₜ depends on BOTH xₜ and hₜ₋₁
- Contrast with feedforward (no horizontal connections)

### **RECOMMENDED GRAPH 6: LSTM Cell Internal Graph**

TikZ diagram showing LSTM gate structure for ONE time step:
```
Inputs: hₜ₋₁, xₜ, cₜ₋₁

         [hₜ₋₁, xₜ] (concatenated)
              │
      ┌───────┼───────┬───────┐
      ↓       ↓       ↓       ↓
     Wf      Wi      Wc      Wo
      ↓       ↓       ↓       ↓
     σ       σ      tanh     σ
      ↓       ↓       ↓       ↓
     fₜ      iₜ      c̃ₜ      oₜ
      │       │       │       │
      └───┬───┴───┐   │       │
          ↓       ↓   ↓       │
    cₜ₋₁ ⊙ fₜ  + iₜ ⊙ c̃ₜ     │
          └───────┴───→ cₜ ───┤
                        │     │
                       tanh   │
                        │     │
                        └──⊙──┘
                           ↓
                          hₜ

Show data flow through gates
Highlight cell state "highway" (cₜ₋₁ → cₜ)
```

**Key features:**
- Show all 4 gates as separate computation nodes
- Show element-wise operations (⊙) explicitly
- Highlight the cell state path (additive, not multiplicative)
- Show which operations are σ vs tanh
- This explains why LSTM helps with vanishing gradients

### **RECOMMENDED GRAPH 7: BPTT Gradient Flow Graph**

Show gradient flow backward through time:
```
Forward (solid arrows):
h₀ ──→ h₁ ──→ h₂ ──→ h₃ ──→ Loss
       ↓      ↓      ↓
       y₁     y₂     y₃

Backward (dashed arrows):
h₀ ←── h₁ ←── h₂ ←── h₃ ←── ∂L
   ∂   ↑  ∂   ↑  ∂   ↑
       y₁     y₂     y₃

Gradient at h₁ comes from TWO sources:
  1. Direct: ∂L/∂y₁ (from output)
  2. Indirect: ∂L/∂h₂ (from future time steps)

Show gradient multiplication through time:
  ∂L/∂h₀ = ∂L/∂h₃ × (∂h₃/∂h₂) × (∂h₂/∂h₁) × (∂h₁/∂h₀)
         = ∂L/∂h₃ × Wₕₕᵀ × Wₕₕᵀ × Wₕₕᵀ
         
This shows why gradients vanish: multiplying Wₕₕᵀ many times!
```

**Location**: Section 6.1 (Vanilla RNNs), Section 6.2 (LSTM), Section 6.1.1 (BPTT)

---

## Chapter 7: Attention Fundamentals

### Current State
- Has attention formula: `cₜ = Σ αₜᵢhᵢ`
- Shows Bahdanau and scaled dot-product attention but **no graph showing attention connections**
- Example 7.3 shows computation but not the network topology

### **RECOMMENDED GRAPH 8: Attention Mechanism as Computational Graph**

TikZ diagram showing attention connections:
```
Encoder hidden states:     Decoder state:     Context vector:
    h₁ ────┐                   s₂                  c₂
    h₂ ────┼────→ [Attention] ←─┘                  ↓
    h₃ ────┘      weights                    (weighted sum)
                  α₂₁, α₂₂, α₂₃                     ↓
                      ↓                          Decoder
    h₁ ──α₂₁──→ ┐
    h₂ ──α₂₂──→ ├─→ Σ ──→ c₂
    h₃ ──α₂₃──→ ┘

Show:
  • Query (s₂) attends to all Keys (h₁, h₂, h₃)
  • Attention weights (α) on edges
  • Weighted sum produces context vector
  • Thickness of arrows proportional to attention weight
```

**Key features:**
- Show that EVERY encoder state connects to the context vector
- Show attention weights as edge labels
- Contrast with RNN encoder-decoder (only final h₃ used)
- Highlight dynamic weighting (different α for each decoder step)

### **RECOMMENDED GRAPH 9: Scaled Dot-Product Attention Computational Graph**

Show the computation flow for attention:
```
Queries (m×dₖ)    Keys (n×dₖ)      Values (n×dᵥ)
     Q                 K                 V
     │                 │                 │
     └────────┬────────┘                 │
              ↓                          │
          QKᵀ/√dₖ                        │
              ↓                          │
          Softmax                        │
              ↓                          │
          Attention                      │
          Weights A                      │
          (m×n)                          │
              │                          │
              └──────────┬───────────────┘
                         ↓
                        AV
                         ↓
                    Output (m×dᵥ)

Each query attends to ALL keys
Result: m output vectors, each a weighted sum of n value vectors
```

**Location**: Section 7.3 (Scaled Dot-Product Attention)
```
Query q = [1.0, 0.5, 0.3]
Keys:  k₁ = [0.8, 0.4, 0.2]
       k₂ = [0.3, 0.9, 0.1]
       k₃ = [0.5, 0.2, 0.7]

Step 1: Compute dot products
  q·k₁ = 1.0×0.8 + 0.5×0.4 + 0.3×0.2 = 0.8+0.2+0.06 = 1.06
  q·k₂ = 1.0×0.3 + 0.5×0.9 + 0.3×0.1 = 0.3+0.45+0.03 = 0.78
  q·k₃ = 1.0×0.5 + 0.5×0.2 + 0.3×0.7 = 0.5+0.1+0.21 = 0.81

Step 2: Scale by √dₖ = √3 = 1.73
  scores = [1.06/1.73, 0.78/1.73, 0.81/1.73]
         = [0.61, 0.45, 0.47]

Step 3: Softmax
  exp_sum = e^0.61 + e^0.45 + e^0.47 = 1.84 + 1.57 + 1.60 = 5.01
  α = [1.84/5.01, 1.57/5.01, 1.60/5.01]
    = [0.37, 0.31, 0.32]

Step 4: Apply to values
  v₁ = [1.0, 0.5], v₂ = [0.3, 0.8], v₃ = [0.6, 0.4]
  output = 0.37×[1.0,0.5] + 0.31×[0.3,0.8] + 0.32×[0.6,0.4]
         = [0.37,0.19] + [0.09,0.25] + [0.19,0.13]
         = [0.65, 0.57]
```

### **RECOMMENDED VISUAL 9: Attention Backpropagation**
```
Forward (must store):
  Q, K, V matrices
  Attention scores S = QKᵀ/√dₖ
  Attention weights A = softmax(S)
  Output O = AV

Backward:
  Given: ∂L/∂O
  
  ∂L/∂V = Aᵀ(∂L/∂O)  [needs A from forward]
  ∂L/∂A = (∂L/∂O)Vᵀ   [needs V from forward]
  ∂L/∂S = softmax_backward(∂L/∂A, A)  [needs A]
  ∂L/∂Q = (∂L/∂S)Kᵀ/√dₖ  [needs K from forward]
  ∂L/∂K = (∂L/∂S)ᵀQ/√dₖ  [needs Q from forward]

MEMORY CRITICAL:
  Attention matrix A: n×n (quadratic in sequence length!)
  For BERT: 512×512×4 bytes = 1MB per head
           ×12 heads = 12MB per layer
           ×12 layers = 144MB per sequence
           ×32 batch = 4.6GB just for attention weights!
```

**Location**: Section 7.3 (Scaled Dot-Product Attention)

---

## Chapter 8: Self-Attention and Multi-Head Attention

### Current State
- Has self-attention formula with Q=K=V=X
- Multi-head attention concatenates heads but **no graph showing parallel attention heads**
- Example 8.2 shows BERT dimensions but not the network topology

### **RECOMMENDED GRAPH 10: Self-Attention Connectivity Pattern**

TikZ diagram showing self-attention connections:
```
Input sequence: x₁, x₂, x₃

Self-attention: Each position attends to ALL positions

     x₁ ──────┬──────┬──────→ output₁
     ↑ ↘      │      │  ↗
     │   ↘    │    ↗ │
     │     ↘  │  ↗   │
     │       ↘↓↗     │
     x₂ ──────┼──────┼──────→ output₂
     ↑        │↘   ↗ │
     │        │  ↘   │
     │        │    ↘ │
     │        │      ↓
     x₃ ──────┴──────┴──────→ output₃

All-to-all connections (n² connections for n tokens)
Each output is weighted sum of ALL inputs
Contrast with RNN: only sequential connections
```

**Key features:**
- Show complete connectivity (every position to every position)
- Highlight that this enables parallelization (no sequential dependency)
- Show that output₁ depends on x₁, x₂, AND x₃ simultaneously
- Contrast with RNN where h₁ only sees x₁

### **RECOMMENDED GRAPH 11: Multi-Head Attention Architecture**

Show parallel attention heads:
```
Input X (seq_len × d_model)
         │
    ┌────┼────┬────┐
    ↓    ↓    ↓    ↓
   Wᵠ¹  Wᵠ²  Wᵠ³  ... (project to dₖ each)
    │    │    │
   Q₁   Q₂   Q₃   (parallel heads)
   K₁   K₂   K₃
   V₁   V₂   V₃
    │    │    │
    ↓    ↓    ↓
  Attn₁ Attn₂ Attn₃  (independent attention computations)
    │    │    │
    └────┼────┴────┐
         ↓         
    [Concat heads]
         ↓
        Wᴼ
         ↓
    Output (seq_len × d_model)

Show that heads compute IN PARALLEL
Each head learns different attention patterns
```

**Location**: Section 8.1 (Self-Attention Mechanism), Section 8.2 (Multi-Head Attention)
```
Input X: [batch=1, seq=3, d=4]

Head 1 (dₖ=2):
  Q₁ = XWᵠ¹ → [3×2]
  K₁ = XWᴷ¹ → [3×2]
  V₁ = XWⱽ¹ → [3×2]
  Attention₁ = softmax(Q₁K₁ᵀ/√2)V₁ → [3×2]

Head 2 (dₖ=2):
  Q₂ = XWᵠ² → [3×2]
  K₂ = XWᴷ² → [3×2]
  V₂ = XWⱽ² → [3×2]
  Attention₂ = softmax(Q₂K₂ᵀ/√2)V₂ → [3×2]

Concatenate:
  [Attention₁; Attention₂] → [3×4]

Output projection:
  Output = [Attention₁; Attention₂]Wᴼ → [3×4]

MEMORY for backprop:
  Must store Q₁,K₁,V₁,Q₂,K₂,V₂ (6 matrices)
  Must store attention weights for both heads
  Must store concatenated result before Wᴼ
```

### **RECOMMENDED VISUAL 11: Positional Encoding Addition**
```
Token embedding: [0.5, 0.3, 0.8, 0.2]
Position 0 PE:   [0.0, 1.0, 0.0, 1.0]
                 ─────────────────────
Input to layer:  [0.5, 1.3, 0.8, 1.2]

Token embedding: [0.4, 0.6, 0.1, 0.9]
Position 1 PE:   [0.84, 0.54, 0.01, 1.0]
                 ─────────────────────
Input to layer:  [1.24, 1.14, 0.11, 1.9]

Shows how position information is injected
```

**Location**: Section 8.1 (Self-Attention Mechanism), Section 8.2 (Multi-Head Attention), Section 8.3 (Positional Encoding)

---

## Chapter 9: Attention Variants

### Current State
- Has cross-attention formula with different Q and K/V sources
- Discusses masking but **no graph showing masked connections**
- Has relative position formulas

### **RECOMMENDED GRAPH 12: Causal Masking Connectivity**

TikZ diagram showing masked vs unmasked attention:
```
UNMASKED (Encoder - bidirectional):
    x₁ ←→ x₂ ←→ x₃ ←→ x₄
    ↕     ↕     ↕     ↕
   All positions can attend to all others

MASKED (Decoder - causal):
    x₁ → x₂ → x₃ → x₄
    ↓    ↓    ↓    ↓
    
Position 1: can only see x₁
Position 2: can see x₁, x₂ (not x₃, x₄)
Position 3: can see x₁, x₂, x₃ (not x₄)
Position 4: can see all

Show with arrows:
  x₁ has 1 incoming arrow (from itself)
  x₂ has 2 incoming arrows (from x₁, x₂)
  x₃ has 3 incoming arrows (from x₁, x₂, x₃)
  x₄ has 4 incoming arrows (from all)

Triangular connectivity pattern!
```

### **RECOMMENDED GRAPH 13: Cross-Attention Architecture**

Show encoder-decoder cross-attention:
```
Encoder outputs:        Decoder:
    h₁ᵉⁿᶜ ────┐
    h₂ᵉⁿᶜ ────┼────→ [Cross-Attn] ←── s₁ᵈᵉᶜ
    h₃ᵉⁿᶜ ────┘         (K,V)         (Q)
                           ↓
                      context c₁
                           ↓
                      next decoder layer

Decoder queries (Q) from decoder state
Keys and Values (K,V) from encoder
Each decoder position attends to ALL encoder positions
```

**Location**: Section 9.1 (Cross-Attention), Section 9.4 (Attention Masking)
```
Attention scores (before masking):
     k₁   k₂   k₃   k₄
q₁ [ 0.8  0.5  0.3  0.6 ]
q₂ [ 0.4  0.9  0.2  0.5 ]
q₃ [ 0.3  0.4  0.7  0.4 ]
q₄ [ 0.6  0.3  0.5  0.8 ]

Apply causal mask (set future to -∞):
     k₁   k₂   k₃   k₄
q₁ [ 0.8  -∞   -∞   -∞  ]
q₂ [ 0.4  0.9  -∞   -∞  ]
q₃ [ 0.3  0.4  0.7  -∞  ]
q₄ [ 0.6  0.3  0.5  0.8 ]

After softmax (row-wise):
     k₁   k₂   k₃   k₄
q₁ [ 1.0  0.0  0.0  0.0 ]  ← can only see position 1
q₂ [ 0.38 0.62 0.0  0.0 ]  ← can see positions 1-2
q₃ [ 0.26 0.29 0.45 0.0 ]  ← can see positions 1-3
q₄ [ 0.27 0.20 0.24 0.29]  ← can see all positions

This prevents "cheating" during training!
```

**Location**: Section 9.4 (Attention Masking)

---

## Chapter 10: Transformer Model

### Current State
- Has complete architecture description
- Shows encoder/decoder layer structure but **no graph showing information flow through layers**
- BERT example has dimensions but not the computational graph

### **RECOMMENDED GRAPH 14: Transformer Encoder Layer Computational Graph**

TikZ diagram showing one encoder layer:
```
Input X (seq_len × d_model)
    │
    ├─────────────────┐ (residual connection)
    ↓                 │
Multi-Head           │
Self-Attention       │
    ↓                 │
    ├←────────────────┘ (add)
    ↓
Layer Norm
    │
    ├─────────────────┐ (residual connection)
    ↓                 │
Feed-Forward         │
(d → 4d → d)         │
    ↓                 │
    ├←────────────────┘ (add)
    ↓
Layer Norm
    ↓
Output (seq_len × d_model)

Show residual paths as curved arrows around main path
Highlight that dimensions stay constant (seq_len × d_model)
```

### **RECOMMENDED GRAPH 15: Complete Transformer Encoder-Decoder Graph**

Show full architecture with stacked layers:
```
Input Tokens
    ↓
Embedding + Positional Encoding
    ↓
┌─────────────────┐
│ Encoder Layer 1 │ ──┐
├─────────────────┤   │
│ Encoder Layer 2 │   │
├─────────────────┤   │ Encoder
│      ...        │   │ Output
├─────────────────┤   │
│ Encoder Layer N │ ──┘
└─────────────────┘
         │
         ├──────────────────────┐
         │                      │
         ↓                      ↓
    (Keys, Values)          Decoder
         │                  Input Tokens
         │                      ↓
         │              Embedding + PE
         │                      ↓
         │              ┌──────────────────┐
         │              │ Masked Self-Attn │
         │              ├──────────────────┤
         └──────────────→ Cross-Attention  │ Layer 1
                        ├──────────────────┤
                        │   Feed-Forward   │
                        └──────────────────┘
                               ↓
                        (repeat N layers)
                               ↓
                        Linear + Softmax
                               ↓
                        Output Probabilities

Show encoder-decoder connection via cross-attention
```

**Location**: Section 10.2 (Transformer Encoder), Section 10.4 (Transformer Decoder)
```
Input X: [batch=1, seq=4, d=512]

1. Multi-Head Self-Attention:
   Q,K,V = XWᵠ, XWᴷ, XWⱽ
   Attention output: [1×4×512]
   
2. Add & Norm:
   X₁ = LayerNorm(X + Attention)
   [Must store X and Attention for backprop]
   
3. Feed-Forward:
   FFN(x) = W₂·ReLU(W₁x + b₁) + b₂
   Hidden: [1×4×2048] (4× expansion)
   Output: [1×4×512]
   [Must store pre-ReLU activations for backprop]
   
4. Add & Norm:
   X₂ = LayerNorm(X₁ + FFN)
   [Must store X₁ and FFN for backprop]

Final output: [1×4×512]

MEMORY BREAKDOWN:
  Attention weights: 4×4 = 16 values
  FFN intermediate: 4×2048 = 8,192 values
  Residual connections: 2× input copies
  Total per layer: ~10KB for this example
  For BERT (512 seq, 768 dim): ~200MB per layer!
```

### **RECOMMENDED VISUAL 14: Encoder-Decoder Cross-Attention**
```
Encoder output (source): [batch=1, src_len=5, d=512]
Decoder state (target):  [batch=1, tgt_len=3, d=512]

Cross-Attention:
  Q = Decoder × Wᵠ  → [1×3×512]  (queries from decoder)
  K = Encoder × Wᴷ  → [1×5×512]  (keys from encoder)
  V = Encoder × Wⱽ  → [1×5×512]  (values from encoder)
  
  Scores = QKᵀ/√dₖ  → [1×3×5]  (decoder × encoder)
  
  Attention weights (after softmax):
       enc₁  enc₂  enc₃  enc₄  enc₅
  dec₁ [0.1  0.6  0.2  0.05 0.05]  ← focuses on enc₂
  dec₂ [0.05 0.1  0.7  0.1  0.05]  ← focuses on enc₃
  dec₃ [0.05 0.05 0.1  0.6  0.2 ]  ← focuses on enc₄
  
  Output = Attention × V → [1×3×512]
  
Each decoder position attends to ALL encoder positions!
```

**Location**: Section 10.2 (Transformer Encoder), Section 10.4 (Transformer Decoder)

---

## Summary of Recommendations

### High Priority (Most Educational Value):
1. **Chapter 4**: MLP computational graph showing neuron connections (Graph 1-2)
2. **Chapter 6**: LSTM internal gate structure graph (Graph 6)
3. **Chapter 7**: Attention mechanism connectivity (Graph 8-9)
4. **Chapter 8**: Self-attention all-to-all connections + multi-head parallel structure (Graph 10-11)
5. **Chapter 10**: Complete transformer layer flow graph (Graph 14-15)

### Medium Priority:
6. **Chapter 5**: Convolutional receptive field connections (Graph 3-4)
7. **Chapter 6**: RNN unrolled through time (Graph 5)
8. **Chapter 9**: Causal masking connectivity pattern (Graph 12-13)

### Lower Priority (But Still Valuable):
9. **Chapter 6**: BPTT gradient flow graph (Graph 7)
10. **Chapter 4**: Backprop gradient flow (Graph 2)

---

## Implementation Notes

### TikZ Graph Design Principles:

1. **Node Representation**:
   - Circles for neurons/activations
   - Rectangles for operations (sum, activation, etc.)
   - Different colors for different layer types

2. **Edge/Arrow Representation**:
   - Solid arrows for forward pass data flow
   - Dashed arrows for backward pass gradient flow
   - Arrow thickness proportional to attention weights (for attention graphs)
   - Edge labels showing weights or dimensions

3. **Layout Strategies**:
   - Left-to-right for feedforward flow
   - Top-to-bottom for layer stacking
   - Curved arrows for residual connections
   - Grouped nodes for parallel operations (multi-head attention)

### Key Educational Principles:

- **Show connectivity patterns**: Which neurons connect to which
- **Highlight architectural differences**: 
  - Fully connected vs local (conv)
  - Sequential (RNN) vs parallel (attention)
  - Bidirectional vs causal (masked)
- **Show information flow**: Follow one path through the network
- **Contrast architectures**: RNN vs Transformer side-by-side
- **Memory implications**: Show what must be stored (different node colors)

### Specific TikZ Features to Use:

```latex
% Example structure for attention graph
\begin{tikzpicture}[
  neuron/.style={circle, draw, minimum size=1cm},
  operation/.style={rectangle, draw, minimum size=0.8cm},
  forward/.style={->, thick},
  backward/.style={->, dashed, red},
  attention/.style={->, blue, line width=\weight}
]

% Nodes
\node[neuron] (x1) at (0,0) {$x_1$};
\node[neuron] (x2) at (0,-2) {$x_2$};
\node[neuron] (out1) at (4,0) {$o_1$};

% Edges with attention weights
\draw[attention] (x1) -- node[above] {$\alpha_{11}$} (out1);
\draw[attention] (x2) -- node[above] {$\alpha_{12}$} (out1);

\end{tikzpicture}
```

### Backpropagation Graph Emphasis:

For each forward graph, create a companion backward graph showing:
- **Gradient flow direction** (reverse of forward)
- **Which forward activations are needed** (highlighted nodes)
- **Memory storage requirements** (annotated)
- **Gradient computation dependencies** (edge labels)

This directly addresses your concern about showing "which information from forward calculation is needed for backprop, affecting memory."
