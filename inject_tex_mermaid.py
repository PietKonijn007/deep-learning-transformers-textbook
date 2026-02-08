#!/usr/bin/env python3
"""
Inject Mermaid architecture diagrams into chapter .tex files.
Each diagram goes right after the first major definition/algorithm is introduced.
Diagrams show: input vectors + dims, weight dims, activations, memory for fwd/bkwd prop.
"""
import re
import os

CHAPTERS_DIR = "chapters"

# ── Diagram definitions ──────────────────────────────────────────────────────
# Each entry: (search_pattern, mermaid_block_to_insert)
# search_pattern: a unique string AFTER which the diagram is inserted
# The mermaid block includes the full \begin{mermaid}...\end{mermaid}

DIAGRAMS = {}

# ── Chapter 4: Feed-Forward Neural Networks ──────────────────────────────────
DIAGRAMS["chapter04_feedforward_networks"] = (
    # Insert after the MLP definition ends
    r"where $\mW^{(\ell)} \in \R^{n_\ell \times n_{\ell-1}}$ is the weight matrix and $\sigma^{(\ell)}$ is the activation function.",
    r"""
\begin{mermaid}[MLP Forward and Backward Pass]
graph LR
    X["Input x\n x in R^n0"] -->|"W1 in R^n1 x n0\n b1 in R^n1"| Z1["Pre-activation\n z1 = W1*x + b1\n z1 in R^n1\n STORED for backprop"]
    Z1 -->|"Activation sigma"| H1["h1 = sigma(z1)\n h1 in R^n1\n STORED for backprop"]
    H1 -->|"W2 in R^n2 x n1\n b2 in R^n2"| Z2["Pre-activation\n z2 = W2*h1 + b2\n z2 in R^n2\n STORED for backprop"]
    Z2 -->|"softmax"| Y["Output y_hat\n y_hat in R^n2"]
    Y --> L["Loss L(y_hat, y)"]

    L -.->|"dL/dz2 needs: z2, y_hat"| Z2
    Z2 -.->|"dL/dW2 needs: h1"| H1
    H1 -.->|"dL/dz1 needs: z1, sigma prime"| Z1
    Z1 -.->|"dL/dW1 needs: x"| X

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style Z1 fill:#fff3e0,stroke:#ff9800,color:#000
    style H1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style Z2 fill:#fff3e0,stroke:#ff9800,color:#000
    style Y fill:#f3e5f5,stroke:#9c27b0,color:#000
    style L fill:#fce4ec,stroke:#e91e63,color:#000
\end{mermaid}
"""
)

# ── Chapter 5: Convolutional Neural Networks ─────────────────────────────────
DIAGRAMS["chapter05_convolutional_networks"] = (
    r"(\mX \star \mK)_{i,j} = \sum_{m=0}^{k_h-1} \sum_{n=0}^{k_w-1} \mX_{i+m, j+n} \cdot \mK_{m,n}",
    r"""
\begin{mermaid}[CNN Forward Pass with Memory]
graph LR
    X["Input\n X in R^H x W x C_in"] -->|"Filters K in R^k x k x C_in x C_out\n bias b in R^C_out"| CONV["Conv2D\n (X * K + b)\n Output in R^H' x W' x C_out\n STORED: X for dL/dK"]
    CONV -->|"ReLU"| ACT["Activation\n ReLU(conv)\n in R^H' x W' x C_out\n STORED: conv for ReLU'"]
    ACT -->|"stride s, pool size p"| POOL["MaxPool\n in R^H'' x W'' x C_out\n STORED: max indices\n for backprop routing"]
    POOL -->|"Flatten"| FLAT["Flat vector\n in R^(H''*W''*C_out)"]
    FLAT -->|"W_fc in R^K x D\n b_fc in R^K"| FC["FC Layer\n z = W_fc * flat + b_fc\n in R^K\n STORED: flat for dL/dW"]
    FC -->|"softmax"| OUT["Output\n y_hat in R^K"]

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style CONV fill:#fff3e0,stroke:#ff9800,color:#000
    style ACT fill:#e3f2fd,stroke:#2196f3,color:#000
    style POOL fill:#fff3e0,stroke:#ff9800,color:#000
    style FC fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

# ── Chapter 6: Recurrent Neural Networks ─────────────────────────────────────
DIAGRAMS["chapter06_recurrent_networks"] = (
    r"\item $\vh_0$ initialized (often zeros)",
    r"""
\begin{mermaid}[RNN/LSTM Forward Pass with Memory]
graph LR
    subgraph TimeStep["Each Timestep t"]
        XT["Input x_t\n in R^d"] -->|"W_xh in R^h x d"| Z["z_t = W_hh*h_t-1\n + W_xh*x_t + b_h\n in R^h"]
        HT_prev["Hidden h_t-1\n in R^h"] -->|"W_hh in R^h x h"| Z
        Z -->|"tanh"| HT["h_t = tanh(z_t)\n in R^h\n STORED: z_t for tanh'\n STORED: h_t-1 for dL/dW_hh\n STORED: x_t for dL/dW_xh"]
        HT -->|"W_hy in R^k x h\n b_y in R^k"| YT["y_t = W_hy*h_t + b_y\n in R^k"]
    end

    subgraph LSTM_Gates["LSTM Gating (Alternative)"]
        FG["Forget Gate f_t\n sigma(W_f*[h_t-1,x_t])\n in R^h -- STORED"]
        IG["Input Gate i_t\n sigma(W_i*[h_t-1,x_t])\n in R^h -- STORED"]
        OG["Output Gate o_t\n sigma(W_o*[h_t-1,x_t])\n in R^h -- STORED"]
        CS["Cell State c_t\n f_t . c_t-1 + i_t . c_tilde\n in R^h -- STORED"]
    end

    style XT fill:#e8f5e9,stroke:#4caf50,color:#000
    style Z fill:#fff3e0,stroke:#ff9800,color:#000
    style HT fill:#e3f2fd,stroke:#2196f3,color:#000
    style YT fill:#f3e5f5,stroke:#9c27b0,color:#000
    style CS fill:#fce4ec,stroke:#e91e63,color:#000
\end{mermaid}
"""
)

# ── Chapter 7: Attention Fundamentals ────────────────────────────────────────
DIAGRAMS["chapter07_attention_fundamentals"] = (
    r"\text{Attention}(\mQ, \mK, \mV) = \text{softmax}\left(\frac{\mQ \mK\transpose}{\sqrt{d_k}}\right) \mV",
    r"""
\begin{mermaid}[Scaled Dot-Product Attention Data Flow]
graph LR
    Q["Queries Q\n in R^m x d_k"] -->|"Matmul Q*K^T"| S["Score Matrix\n E = Q*K^T\n in R^m x n\n STORED for backprop"]
    K["Keys K\n in R^n x d_k"] --> S
    S -->|"Scale by 1/sqrt(d_k)"| SC["Scaled Scores\n E / sqrt(d_k)\n in R^m x n"]
    SC -->|"Softmax (row-wise)"| A["Attention Weights\n A = softmax(E_scaled)\n in R^m x n\n STORED: A for dL/dV\n STORED: softmax input for backprop"]
    A -->|"Matmul A*V"| OUT["Output\n A*V in R^m x d_v\n STORED: A for dL/dV\n STORED: V for dL/dA"]
    V["Values V\n in R^n x d_v"] --> OUT

    style Q fill:#e3f2fd,stroke:#2196f3,color:#000
    style K fill:#e8f5e9,stroke:#4caf50,color:#000
    style V fill:#fff3e0,stroke:#ff9800,color:#000
    style A fill:#f3e5f5,stroke:#9c27b0,color:#000
    style OUT fill:#fce4ec,stroke:#e91e63,color:#000
\end{mermaid}
"""
)

# ── Chapter 8: Self-Attention and Multi-Head Attention ───────────────────────
DIAGRAMS["chapter08_self_attention"] = (
    r"where $\mW^{Q(i)}, \mW^{K(i)}, \mW^{V(i)} \in \R^{d_{\text{model}} \times d_k}$ and $\mW^O \in \R^{hd_k \times d_{\text{model}}}$.",
    r"""
\begin{mermaid}[Multi-Head Self-Attention Data Flow]
graph LR
    X["Input X\n in R^n x d_model"] -->|"W_Q^i in R^d_model x d_k\n per head"| Q["Q_i = X*W_Q^i\n in R^n x d_k\n STORED: X for dL/dW_Q"]
    X -->|"W_K^i in R^d_model x d_k"| K["K_i = X*W_K^i\n in R^n x d_k"]
    X -->|"W_V^i in R^d_model x d_v"| V["V_i = X*W_V^i\n in R^n x d_v"]
    Q --> ATT["Attention(Q_i,K_i,V_i)\n softmax(Q_i*K_i^T/sqrt(d_k))*V_i\n head_i in R^n x d_v\n h heads in parallel\n STORED: attn weights per head"]
    K --> ATT
    V --> ATT
    ATT -->|"Concat h heads"| CAT["[head_1;...;head_h]\n in R^n x h*d_v"]
    CAT -->|"W_O in R^(h*d_v) x d_model"| OUT["Output\n in R^n x d_model\n STORED: concat for dL/dW_O"]

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style Q fill:#e3f2fd,stroke:#2196f3,color:#000
    style K fill:#e3f2fd,stroke:#2196f3,color:#000
    style V fill:#e3f2fd,stroke:#2196f3,color:#000
    style ATT fill:#fff3e0,stroke:#ff9800,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

# ── Chapter 9: Attention Variants ────────────────────────────────────────────
DIAGRAMS["chapter09_attention_variants"] = (
    r"\textbf{Dimensions:}",
    r"""
\begin{mermaid}[Cross-Attention vs Self-Attention Data Flow]
graph LR
    subgraph SelfAttn["Self-Attention"]
        SX["X in R^n x d"] -->|"W_Q, W_K, W_V"| SQ["Q,K,V all\n from X\n Memory: O(n^2)"]
        SQ --> SOUT["Output in R^n x d"]
    end

    subgraph CrossAttn["Cross-Attention (Encoder-Decoder)"]
        DX["Decoder X_dec\n in R^m x d"] -->|"W_Q in R^d x d_k"| CQ["Q = X_dec * W_Q\n in R^m x d_k"]
        EX["Encoder X_enc\n in R^n x d"] -->|"W_K in R^d x d_k\n W_V in R^d x d_v"| CKV["K in R^n x d_k\n V in R^n x d_v"]
        CQ --> COUT["Attn(Q,K,V)\n in R^m x d_v\n Memory: O(m*n)\n STORED: Q,K,V,attn_weights"]
        CKV --> COUT
    end

    style SX fill:#e8f5e9,stroke:#4caf50,color:#000
    style DX fill:#e3f2fd,stroke:#2196f3,color:#000
    style EX fill:#e8f5e9,stroke:#4caf50,color:#000
    style COUT fill:#fff3e0,stroke:#ff9800,color:#000
\end{mermaid}
"""
)

# ── Chapter 10: Transformer Model ────────────────────────────────────────────
DIAGRAMS["chapter10_transformer_model"] = (
    r"with $\mW_1 \in \R^{d_{\text{model}} \times d_{ff}}$, $\mW_2 \in \R^{d_{ff} \times d_{\text{model}}}$, and typically $d_{ff} = 4 \times d_{\text{model}}$.",
    r"""
\begin{mermaid}[Transformer Encoder Layer Forward Pass]
graph LR
    X["Input X\n in R^n x d_model"] --> MHA["Multi-Head\n Self-Attention\n STORED: Q,K,V,\n attn_weights\n for backprop"]
    MHA --> ADD1["Residual Add\n X + MHA(X)"]
    ADD1 --> LN1["LayerNorm\n in R^n x d_model\n STORED: mean, var\n for backprop"]
    LN1 -->|"W1 in R^d_model x d_ff\n b1 in R^d_ff"| FFN1["Linear + ReLU\n ReLU(W1*x + b1)\n in R^n x d_ff\n STORED: pre-ReLU\n for backprop"]
    FFN1 -->|"W2 in R^d_ff x d_model\n b2 in R^d_model"| FFN2["Linear\n W2*h + b2\n in R^n x d_model\n STORED: h for dL/dW2"]
    FFN2 --> ADD2["Residual Add\n LN1 + FFN"]
    ADD2 --> LN2["LayerNorm\n Output in R^n x d_model\n STORED: mean, var"]

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style MHA fill:#fff3e0,stroke:#ff9800,color:#000
    style LN1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style FFN1 fill:#fff3e0,stroke:#ff9800,color:#000
    style FFN2 fill:#e3f2fd,stroke:#2196f3,color:#000
    style LN2 fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

# ── Chapter 11: Training Transformers ────────────────────────────────────────
DIAGRAMS["chapter11_training_transformers"] = (
    r"\section{Training Objectives and Loss Functions}",
    r"""
\begin{mermaid}[Transformer Training Pipeline]
graph LR
    D["Raw Text"] -->|"BPE/WordPiece"| TOK["Token IDs\n in N^B x n"]
    TOK -->|"Embedding\n W_emb in R^V x d"| EMB["Embeddings\n + Positional Enc\n in R^B x n x d\n STORED for backprop"]
    EMB --> TF["Transformer\n Layers x L\n STORED per layer:\n activations, attn\n weights, LN stats"]
    TF -->|"W_head in R^d x V"| LM["LM Head\n logits in R^B x n x V\n STORED for softmax backprop"]
    LM -->|"Cross-Entropy"| LOSS["Loss\n sum(-y*log(p))"]
    LOSS -.->|"Backward:\n peak memory =\n O(L * n * d + n^2 * h)"| TF
    LOSS -.->|"AdamW step:\n 2x param memory\n for m_t, v_t states"| OPT["Optimizer\n theta -= lr * update"]

    style D fill:#e8f5e9,stroke:#4caf50,color:#000
    style TF fill:#fff3e0,stroke:#ff9800,color:#000
    style LM fill:#e3f2fd,stroke:#2196f3,color:#000
    style LOSS fill:#fce4ec,stroke:#e91e63,color:#000
    style OPT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)

# ── Chapter 12: Computational Analysis ───────────────────────────────────────
DIAGRAMS["chapter12_computational_analysis"] = (
    r"\subsection{Self-Attention Complexity}",
    r"""
\begin{mermaid}[Transformer Computation and Memory per Layer]
graph LR
    subgraph Compute["FLOPs per Layer"]
        SA["Self-Attention\n Q*K^T: O(n^2 * d_k)\n A*V: O(n^2 * d_v)\n Projections: O(n * d^2)"]
        FF["Feed-Forward\n W1: O(n * d * d_ff)\n W2: O(n * d_ff * d)\n Total: O(n * d * d_ff)"]
    end

    subgraph Memory["Memory per Layer"]
        AM["Attention Matrix\n n x n floats\n O(n^2) memory\n DOMINATES for long seq"]
        WM["Weight Memory\n W_Q,W_K,W_V,W_O: 4*d^2\n W1,W2: 2*d*d_ff\n O(d^2) per layer"]
        ACT["Activation Memory\n Stored for backprop:\n X, Q, K, V, A,\n FFN intermediate\n O(n*d + n^2) per layer"]
    end

    SA --> AM
    FF --> WM
    SA --> ACT
    FF --> ACT

    style SA fill:#fff3e0,stroke:#ff9800,color:#000
    style FF fill:#e3f2fd,stroke:#2196f3,color:#000
    style AM fill:#fce4ec,stroke:#e91e63,color:#000
    style ACT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)

# ── Chapter 13: BERT ─────────────────────────────────────────────────────────
DIAGRAMS["chapter13_bert"] = (
    r"\item \textbf{Output:} Contextualized representations for all tokens",
    r"""
\begin{mermaid}[BERT Architecture Data Flow]
graph LR
    TOK["[CLS] tok1 [MASK] tok3 [SEP]\n Token IDs in N^n"] -->|"Token Emb\n W_tok in R^V x d"| TE["Token Emb\n in R^n x d"]
    SEG["Segment IDs\n in {0,1}^n"] -->|"Segment Emb\n W_seg in R^2 x d"| SE["Seg Emb\n in R^n x d"]
    POS["Position 0..n-1"] -->|"Pos Emb\n W_pos in R^n_max x d"| PE["Pos Emb\n in R^n x d"]

    TE --> ADD["Sum Embeddings\n E = Tok + Seg + Pos\n in R^n x d\n STORED for backprop"]
    SE --> ADD
    PE --> ADD

    ADD --> ENC["Transformer Encoder\n x L layers (12 or 24)\n Each: MHA + FFN + LN\n STORED per layer:\n attn weights, activations"]

    ENC -->|"[CLS] output"| CLS["CLS repr\n in R^d --> NSP head\n W_nsp in R^d x 2"]
    ENC -->|"masked positions"| MLM["Masked outputs\n in R^k x d --> MLM head\n W_mlm in R^d x V\n STORED for cross-entropy backprop"]

    style TOK fill:#e8f5e9,stroke:#4caf50,color:#000
    style ADD fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#fff3e0,stroke:#ff9800,color:#000
    style CLS fill:#f3e5f5,stroke:#9c27b0,color:#000
    style MLM fill:#fce4ec,stroke:#e91e63,color:#000
\end{mermaid}
"""
)

# ── Chapter 14: GPT ──────────────────────────────────────────────────────────
DIAGRAMS["chapter14_gpt"] = (
    r"\item \textbf{Pre-norm:} Layer norm before sub-layers (GPT-2+)",
    r"""
\begin{mermaid}[GPT Decoder-Only Architecture]
graph LR
    TOK["Input tokens\n x_1..x_t\n in N^t"] -->|"W_emb in R^V x d\n + W_pos in R^n_max x d"| EMB["Token + Pos Emb\n in R^t x d\n STORED for backprop"]
    EMB --> DEC["Decoder Layers x L\n Each layer:\n 1. Masked Self-Attn\n (causal mask: upper tri = -inf)\n STORED: Q,K,V,attn,mask\n 2. FFN: W1 in R^d x 4d,\n W2 in R^4d x d\n STORED: activations"]
    DEC -->|"W_head in R^d x V\n (often tied with W_emb)"| LM["LM Head\n logits in R^t x V"]
    LM -->|"softmax"| PRED["P(x_t+1 | x_1..x_t)\n in R^V\n STORED: logits for\n cross-entropy backprop"]

    PRED -.->|"Backprop:\n dL/dlogits --> dL/dW_head\n --> through L decoder layers\n peak memory: O(L*t*d + L*t^2)"| EMB

    style TOK fill:#e8f5e9,stroke:#4caf50,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style DEC fill:#fff3e0,stroke:#ff9800,color:#000
    style LM fill:#f3e5f5,stroke:#9c27b0,color:#000
    style PRED fill:#fce4ec,stroke:#e91e63,color:#000
\end{mermaid}
"""
)

# ── Chapter 15: T5 and BART ──────────────────────────────────────────────────
DIAGRAMS["chapter15_t5_bart"] = (
    r"\subsection{T5 Architecture}",
    r"""
\begin{mermaid}[T5 Encoder-Decoder Architecture]
graph LR
    SRC["Source text\n tokens in N^n"] -->|"Shared W_emb\n in R^V x d\n + Relative Pos Bias"| EEMB["Encoder Emb\n in R^n x d"]
    EEMB --> ENC["Encoder x L layers\n Self-Attn + FFN\n STORED: all activations\n Output in R^n x d"]

    TGT["Target prefix\n tokens in N^m"] -->|"Shared W_emb"| DEMB["Decoder Emb\n in R^m x d"]
    DEMB --> DSAL["Decoder x L layers\n 1. Causal Self-Attn\n 2. Cross-Attn to Encoder\n 3. FFN\n STORED: Q,K,V per layer\n + cross-attn K,V from encoder"]
    ENC --> DSAL

    DSAL -->|"W_head in R^d x V"| OUT["Output logits\n in R^m x V\n STORED for backprop"]

    style SRC fill:#e8f5e9,stroke:#4caf50,color:#000
    style ENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style DSAL fill:#fff3e0,stroke:#ff9800,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)

# ── Chapter 16: Efficient Transformers ───────────────────────────────────────
DIAGRAMS["chapter16_efficient_transformers"] = (
    r"Three fundamental patterns have emerged as particularly effective building blocks for sparse attention.",
    r"""
\begin{mermaid}[Efficient Attention Approaches and Memory]
graph LR
    FULL["Full Attention\n A = softmax(QK^T/sqrt(d))V\n Compute: O(n^2 d)\n Memory: O(n^2)\n STORED: full n x n matrix"]

    FULL --> SPARSE["Sparse Attention\n Only compute S subset\n of n^2 entries\n Memory: O(n * w)\n w = window size"]
    FULL --> LINEAR["Linear Attention\n phi(Q)*[phi(K)^T * V]\n Compute: O(n * d^2)\n Memory: O(n * d)\n NO n x n matrix stored"]
    FULL --> FLASH["FlashAttention\n Tiled computation\n Recompute in backward\n Peak memory: O(n)\n IO-aware: minimizes\n HBM reads/writes"]

    SPARSE --> SP1["Longformer: local w\n + global g tokens\n O(n*(w+g))"]
    LINEAR --> LIN1["Performer: random\n feature map phi\n O(n*d*r), r = features"]

    style FULL fill:#fce4ec,stroke:#e91e63,color:#000
    style SPARSE fill:#e3f2fd,stroke:#2196f3,color:#000
    style LINEAR fill:#e8f5e9,stroke:#4caf50,color:#000
    style FLASH fill:#fff3e0,stroke:#ff9800,color:#000
\end{mermaid}
"""
)

# ── Chapter 17: Vision Transformers ──────────────────────────────────────────
DIAGRAMS["chapter17_vision_transformers"] = (
    r"\mX = \mX + \mE_{\text{pos}}",
    r"""
\begin{mermaid}[Vision Transformer (ViT) Forward Pass]
graph LR
    IMG["Image I\n in R^H x W x C"] -->|"Split P x P patches"| PAT["N = HW/P^2 patches\n each in R^(P^2*C)"]
    PAT -->|"W_patch in R^(P^2*C) x d\n b in R^d"| EMB["Patch Embeddings\n in R^N x d\n STORED for dL/dW_patch"]
    CLS["[CLS] token\n learnable in R^d"] --> CAT["Prepend [CLS]\n in R^(N+1) x d"]
    EMB --> CAT
    POS["Position Emb\n E_pos in R^(N+1) x d"] --> ADD["Add Pos Emb\n in R^(N+1) x d"]
    CAT --> ADD
    ADD --> ENC["Transformer Encoder\n x L layers\n MHA + FFN + LN\n STORED per layer:\n activations, attn weights\n Memory: O(L*(N+1)^2 + L*(N+1)*d)"]
    ENC -->|"[CLS] output"| HEAD["MLP Head\n W in R^d x K\n Output in R^K"]

    style IMG fill:#e8f5e9,stroke:#4caf50,color:#000
    style PAT fill:#e3f2fd,stroke:#2196f3,color:#000
    style EMB fill:#fff3e0,stroke:#ff9800,color:#000
    style ENC fill:#fff3e0,stroke:#ff9800,color:#000
    style HEAD fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

# ── Chapter 1: Linear Algebra ────────────────────────────────────────────────
DIAGRAMS["chapter01_linear_algebra"] = (
    r"The dimension $n$ is the number of components in the vector.",
    r"""
\begin{mermaid}[Linear Transformation in Neural Networks]
graph LR
    X["Input x\n in R^n"] -->|"Weight W in R^m x n\n Bias b in R^m"| Z["z = Wx + b\n in R^m\n STORED: x for dL/dW\n STORED: z for activation backprop"]
    Z -->|"Activation sigma"| H["h = sigma(z)\n in R^m\n Forward: store z\n Backward: needs sigma'(z)"]

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style Z fill:#fff3e0,stroke:#ff9800,color:#000
    style H fill:#e3f2fd,stroke:#2196f3,color:#000
\end{mermaid}
"""
)

# ── Chapter 2: Calculus and Optimization ─────────────────────────────────────
DIAGRAMS["chapter02_calculus_optimization"] = (
    r"\begin{example}[Computing Partial Derivatives]",
    r"""
\begin{mermaid}[Gradient Descent with Backpropagation]
graph LR
    T["Parameters theta\n in R^p"] -->|"Forward pass"| F["f(x; theta)\n Compute loss L\n STORED: all intermediates\n z_l, h_l per layer"]
    F --> L["Loss L(y_hat, y)\n scalar"]
    L -->|"Backward pass\n chain rule"| G["Gradients\n dL/d_theta in R^p\n Uses stored z_l, h_l\n Memory: O(L * n * d)"]
    G -->|"theta -= eta * dL/d_theta\n eta = learning rate"| T

    style T fill:#e8f5e9,stroke:#4caf50,color:#000
    style F fill:#fff3e0,stroke:#ff9800,color:#000
    style L fill:#fce4ec,stroke:#e91e63,color:#000
    style G fill:#e3f2fd,stroke:#2196f3,color:#000
\end{mermaid}

"""
)

# ── Chapter 3: Probability and Information Theory ────────────────────────────
DIAGRAMS["chapter03_probability_information"] = (
    r"\begin{definition}[Probability Mass Function (PMF)]",
    r"""
\begin{mermaid}[Cross-Entropy Loss in Classification]
graph LR
    X["Input x\n in R^d"] -->|"Model f(x;theta)"| LOGITS["Logits z\n in R^K\n STORED for backprop"]
    LOGITS -->|"softmax"| P["Predicted P(y|x)\n p_k = exp(z_k)/sum\n in R^K\n STORED: p for gradient"]
    Y["True label y\n one-hot in R^K"] --> CE["Cross-Entropy\n H(y,p) = -sum(y_k log p_k)\n = -log p_y\n scalar"]
    P --> CE
    CE -.->|"dL/dz_k = p_k - y_k\n simple gradient"| LOGITS

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style LOGITS fill:#fff3e0,stroke:#ff9800,color:#000
    style P fill:#e3f2fd,stroke:#2196f3,color:#000
    style CE fill:#fce4ec,stroke:#e91e63,color:#000
\end{mermaid}

"""
)

# ── Chapter 18: Multimodal Transformers ──────────────────────────────────────
DIAGRAMS["chapter18_multimodal_transformers"] = (
    r"\begin{figure}[htbp]",
    r"""
\begin{mermaid}[Multimodal Transformer Fusion]
graph LR
    TXT["Text tokens\n in N^n_t"] -->|"W_text in R^V x d"| TE["Text Emb\n in R^n_t x d"]
    IMG["Image patches\n in R^N x (P^2*C)"] -->|"W_img in R^(P^2*C) x d"| IE["Image Emb\n in R^N x d"]

    TE --> FUSE["Concatenate\n [text; image]\n in R^(n_t+N) x d"]
    IE --> FUSE
    FUSE --> ENC["Joint Transformer\n x L layers\n Cross-modal attention\n STORED per layer:\n all activations\n Memory: O(L*(n_t+N)^2)"]
    ENC --> TOUT["Text output\n in R^n_t x d"]
    ENC --> IOUT["Image output\n in R^N x d"]

    style TXT fill:#e8f5e9,stroke:#4caf50,color:#000
    style IMG fill:#e3f2fd,stroke:#2196f3,color:#000
    style FUSE fill:#fff3e0,stroke:#ff9800,color:#000
    style ENC fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)

# ── Chapter 19: Long Context ─────────────────────────────────────────────────
DIAGRAMS["chapter19_long_context"] = (
    r"\begin{example}[Memory Scaling Analysis]",
    r"""
\begin{mermaid}[Long Context Attention Strategies]
graph LR
    SEQ["Long sequence\n n >> 4096 tokens\n Full attn memory:\n O(n^2) -- infeasible"]

    SEQ --> SW["Sliding Window\n w neighbors each side\n Memory: O(n*w)\n STORED: local attn\n weights only"]
    SEQ --> CHUNK["Chunked Attention\n Split into n/c chunks\n Intra-chunk: O(c^2)\n Cross-chunk: summary\n STORED: chunk summaries"]
    SEQ --> ROPE["RoPE Scaling\n Rotary Pos Emb\n Extend via interpolation\n No extra memory\n STORED: same as base"]

    style SEQ fill:#fce4ec,stroke:#e91e63,color:#000
    style SW fill:#e3f2fd,stroke:#2196f3,color:#000
    style CHUNK fill:#e8f5e9,stroke:#4caf50,color:#000
    style ROPE fill:#fff3e0,stroke:#ff9800,color:#000
\end{mermaid}

"""
)

# ── Chapter 20: Pretraining Strategies ───────────────────────────────────────
DIAGRAMS["chapter20_pretraining_strategies"] = (
    r"\subsection{Denoising Objectives}",
    r"""
\begin{mermaid}[Pre-training Objectives Comparison]
graph LR
    subgraph CLM["Causal LM (GPT)"]
        C1["x_1..x_t"] -->|"Predict next"| C2["P(x_t+1|x_leq_t)\n Causal mask\n Memory: O(t^2) attn"]
    end

    subgraph MLM_["Masked LM (BERT)"]
        M1["x with 15% [MASK]"] -->|"Predict masked"| M2["P(x_mask|x_visible)\n Bidirectional\n Memory: O(n^2) attn"]
    end

    subgraph S2S["Seq2Seq (T5)"]
        S1["Corrupted input"] -->|"Encoder"| S2["Enc repr\n in R^n x d"]
        S2 -->|"Decoder"| S3["Reconstruct spans\n Cross-attn memory:\n O(m*n) extra"]
    end

    style C2 fill:#e3f2fd,stroke:#2196f3,color:#000
    style M2 fill:#e8f5e9,stroke:#4caf50,color:#000
    style S3 fill:#fff3e0,stroke:#ff9800,color:#000
\end{mermaid}

"""
)

# ── Chapter 21: PyTorch Implementation ───────────────────────────────────────
DIAGRAMS["chapter21_pytorch_implementation"] = (
    r"\end{itemize}",
    r"""
\begin{mermaid}[PyTorch Transformer Module Hierarchy]
graph LR
    TF["Transformer\n nn.Module"] --> ENC["Encoder\n N x EncoderLayer"]
    TF --> DEC["Decoder\n N x DecoderLayer"]
    TF --> EMB["Embedding\n nn.Embedding(V, d)\n params: V*d"]
    TF --> HEAD["LM Head\n nn.Linear(d, V)\n params: d*V"]

    ENC --> ELYR["EncoderLayer\n Self-Attn + FFN + LN"]
    ELYR --> MHA["MultiHeadAttn\n W_Q,W_K,W_V: 3*d^2\n W_O: d^2\n params: 4*d^2"]
    ELYR --> FFN["FFN\n W1: d*4d, W2: 4d*d\n params: 8*d^2"]
    ELYR --> LN["LayerNorm\n gamma, beta: 2*d"]

    DEC --> DLYR["DecoderLayer\n Masked Self-Attn\n + Cross-Attn + FFN"]

    style TF fill:#e8f5e9,stroke:#4caf50,color:#000
    style ELYR fill:#e3f2fd,stroke:#2196f3,color:#000
    style MHA fill:#fff3e0,stroke:#ff9800,color:#000
    style FFN fill:#fff3e0,stroke:#ff9800,color:#000
\end{mermaid}
"""
)

# ── Chapter 22: Hardware Optimization ────────────────────────────────────────
DIAGRAMS["chapter22_hardware_optimization"] = (
    # Find end of Arithmetic Intensity definition
    r"\end{definition}",
    r"""
\begin{mermaid}[GPU Memory Hierarchy and Optimization]
graph LR
    PARAM["Model Params\n W in R^P\n FP16: 2P bytes"] --> HBM["HBM (GPU RAM)\n 40-80 GB\n Bandwidth: 2 TB/s\n Stores: params, grads,\n optimizer states, activations"]
    HBM --> SRAM["SRAM (On-chip)\n ~20 MB per SM\n Bandwidth: 19 TB/s\n Stores: tiles of Q,K,V\n during FlashAttention"]

    subgraph Optim["Memory Optimizations"]
        MP["Mixed Precision\n FP32 master weights\n FP16 forward/backward\n Saves ~50% memory"]
        GC["Gradient Checkpointing\n Discard activations\n Recompute in backward\n Saves O(L) memory\n Costs ~33% extra compute"]
        FSDP["FSDP/ZeRO\n Shard params+grads+opt\n across N GPUs\n Memory: O(P/N) per GPU"]
    end

    HBM --> Optim

    style PARAM fill:#e8f5e9,stroke:#4caf50,color:#000
    style HBM fill:#fff3e0,stroke:#ff9800,color:#000
    style SRAM fill:#e3f2fd,stroke:#2196f3,color:#000
    style GC fill:#fce4ec,stroke:#e91e63,color:#000
\end{mermaid}
"""
)

# ── Chapter 23: Best Practices ───────────────────────────────────────────────
DIAGRAMS["chapter23_best_practices"] = (
    r"\subsection{Model Size Selection}",
    r"""
\begin{mermaid}[Model Development Pipeline]
graph LR
    DATA["Data\n Train/Val/Test\n splits"] -->|"Tokenize"| TOK["Token IDs\n Vocab V"]
    TOK --> BASE["Baseline Model\n small config\n Validate loss"]
    BASE -->|"Scale up"| TRAIN["Full Training\n STORED in memory:\n Params: 2P bytes (FP16)\n Grads: 2P bytes\n Adam states: 8P bytes\n Activations: O(L*n*d)"]
    TRAIN -->|"Evaluate"| EVAL["Metrics\n Loss, Perplexity\n Task accuracy"]
    EVAL -->|"Tune"| HP["Hyperparams\n lr, warmup, wd\n batch size"]
    HP --> TRAIN

    style DATA fill:#e8f5e9,stroke:#4caf50,color:#000
    style TRAIN fill:#fff3e0,stroke:#ff9800,color:#000
    style EVAL fill:#e3f2fd,stroke:#2196f3,color:#000
\end{mermaid}

"""
)

# ── Chapters 24-34: Domain applications ──────────────────────────────────────
DIAGRAMS["chapter24_domain_specific_models"] = (
    r"\subsection{Example: Legal Document Analysis}",
    r"""
\begin{mermaid}[Domain Adaptation Pipeline]
graph LR
    BASE["Pre-trained LM\n params in R^P"] -->|"Domain corpus"| DAPT["Domain-Adaptive\n Pre-training\n Continue MLM/CLM\n on domain text\n STORED: same as base"]
    DAPT -->|"Task data"| FT["Fine-tuning\n Task-specific head\n W_task in R^d x K\n STORED: all activations\n for backprop"]
    FT --> DEPLOY["Domain Model\n e.g. BioBERT,\n LegalBERT, FinBERT"]

    style BASE fill:#e8f5e9,stroke:#4caf50,color:#000
    style DAPT fill:#fff3e0,stroke:#ff9800,color:#000
    style FT fill:#e3f2fd,stroke:#2196f3,color:#000
    style DEPLOY fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)

DIAGRAMS["chapter25_enterprise_nlp"] = (
    r"\item \textbf{Retrieve top-k:}",
    r"""
\begin{mermaid}[RAG Pipeline Architecture]
graph LR
    Q["Query\n in text"] -->|"Encoder\n W_enc in R^V x d"| QE["Query Emb\n in R^d"]
    DOCS["Document Store\n N docs"] -->|"Encoder"| DE["Doc Embs\n in R^N x d\n Pre-computed"]
    QE -->|"Similarity\n cos(q, d_i)"| RET["Top-K Retrieval\n K docs in R^K x d"]
    DE --> RET
    RET --> GEN["Generator LLM\n Context = query + K docs\n Attn memory: O((n_q+K*n_d)^2)\n STORED: full activations"]
    GEN --> ANS["Answer\n Generated text"]

    style Q fill:#e8f5e9,stroke:#4caf50,color:#000
    style RET fill:#fff3e0,stroke:#ff9800,color:#000
    style GEN fill:#e3f2fd,stroke:#2196f3,color:#000
    style ANS fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)

DIAGRAMS["chapter26_code_language"] = (
    r"A natural language model might compress English text to 0.7 tokens per word on average",
    r"""
\begin{mermaid}[Code Language Model Architecture]
graph LR
    CODE["Source Code\n raw text"] -->|"BPE tokenizer\n V = 32K-50K"| TOK["Code Tokens\n in N^n"]
    TOK -->|"W_emb in R^V x d"| EMB["Embeddings\n + Pos Enc\n in R^n x d"]
    EMB --> DEC["Decoder Layers\n Causal Self-Attn\n + FFN x L layers\n STORED: activations\n for fill-in-middle\n and next-token pred"]
    DEC -->|"W_head in R^d x V"| OUT["Logits in R^n x V\n Predict next token\n or infill [MASK]"]

    style CODE fill:#e8f5e9,stroke:#4caf50,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style DEC fill:#fff3e0,stroke:#ff9800,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

DIAGRAMS["chapter27_video_visual"] = (
    r"Key equations:",
    r"""
\begin{mermaid}[Video Transformer Architecture]
graph LR
    VID["Video\n T x H x W x C\n T frames"] -->|"Per-frame patches\n P x P"| PAT["Patches\n T*N per-frame\n each in R^(P^2*C)"]
    PAT -->|"W_patch in R^(P^2*C) x d"| EMB["Space-Time Emb\n in R^(T*N) x d\n + temporal pos enc"]
    EMB --> SENC["Spatial Encoder\n per-frame self-attn\n O(N^2) per frame\n STORED: spatial attn"]
    SENC --> TENC["Temporal Encoder\n cross-frame attn\n O(T^2) per position\n STORED: temporal attn"]
    TENC --> OUT["Video repr\n in R^(T*N) x d"]

    style VID fill:#e8f5e9,stroke:#4caf50,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style SENC fill:#fff3e0,stroke:#ff9800,color:#000
    style TENC fill:#fff3e0,stroke:#ff9800,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

DIAGRAMS["chapter28_knowledge_graphs"] = (
    r"Knowledge graphs are semi-formal",
    r"""
\begin{mermaid}[Knowledge-Enhanced Transformer]
graph LR
    TXT["Text input\n tokens in N^n"] -->|"W_emb in R^V x d"| TE["Text Emb\n in R^n x d"]
    KG["Knowledge Graph\n entities + relations"] -->|"Entity Emb\n W_ent in R^E x d"| KE["Entity Emb\n in R^k x d"]

    TE --> FUSE["Knowledge Fusion\n Inject entity emb\n at linked positions\n in R^n x d"]
    KE --> FUSE
    FUSE --> ENC["Transformer Encoder\n x L layers\n STORED: activations\n + entity attention"]
    ENC --> OUT["Enhanced repr\n in R^n x d"]

    style TXT fill:#e8f5e9,stroke:#4caf50,color:#000
    style KG fill:#e3f2fd,stroke:#2196f3,color:#000
    style FUSE fill:#fff3e0,stroke:#ff9800,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

DIAGRAMS["chapter29_recommendations"] = (
    r"the model learns that action movies have high probability for the next interaction",
    r"""
\begin{mermaid}[Sequential Recommendation Transformer]
graph LR
    HIST["User history\n item_1..item_t\n IDs in N^t"] -->|"W_item in R^I x d\n + W_pos in R^n x d"| EMB["Item Emb\n in R^t x d"]
    EMB --> ENC["Transformer Encoder\n Causal self-attn\n x L layers\n STORED: attn weights\n per layer for backprop"]
    ENC -->|"Last position output"| REP["User repr\n in R^d"]
    REP -->|"dot product with\n all item embs\n W_item^T in R^d x I"| SCORE["Scores\n in R^I"]
    SCORE -->|"softmax"| TOP["Top-K items\n Recommendations"]

    style HIST fill:#e8f5e9,stroke:#4caf50,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#fff3e0,stroke:#ff9800,color:#000
    style TOP fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

DIAGRAMS["chapter30_healthcare"] = (
    r"Clinical language differs from general English",
    r"""
\begin{mermaid}[Clinical NLP Pipeline]
graph LR
    EHR["Clinical Notes\n free text"] -->|"De-identification\n PHI removal"| CLEAN["Clean text\n HIPAA compliant"]
    CLEAN -->|"Domain tokenizer"| TOK["Tokens in N^n"]
    TOK --> MODEL["ClinicalBERT\n Encoder x L layers\n Pre-trained on MIMIC\n STORED: activations"]
    MODEL -->|"Task head\n W in R^d x K"| OUT["NER / Diagnosis\n predictions"]

    style EHR fill:#e8f5e9,stroke:#4caf50,color:#000
    style CLEAN fill:#e3f2fd,stroke:#2196f3,color:#000
    style MODEL fill:#fff3e0,stroke:#ff9800,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

DIAGRAMS["chapter31_finance"] = (
    r"attention weights provide interpretability",
    r"""
\begin{mermaid}[Financial Time Series Transformer]
graph LR
    TS["Price/Volume\n x_1..x_T\n in R^T x F\n F features"] -->|"W_proj in R^F x d"| EMB["Temporal Emb\n in R^T x d\n + time pos enc"]
    NEWS["News text\n tokens in N^n"] -->|"W_emb in R^V x d"| NE["News Emb\n in R^n x d"]
    EMB --> CROSS["Cross-modal Attn\n Time attends to news\n Memory: O(T*n)\n STORED: attn weights"]
    NE --> CROSS
    CROSS --> PRED["Prediction Head\n W in R^d x 1\n price / sentiment"]

    style TS fill:#e8f5e9,stroke:#4caf50,color:#000
    style NEWS fill:#e3f2fd,stroke:#2196f3,color:#000
    style CROSS fill:#fff3e0,stroke:#ff9800,color:#000
    style PRED fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}
"""
)

DIAGRAMS["chapter32_legal"] = (
    r"\subsection{Formal Language Elements}",
    r"""
\begin{mermaid}[Legal Document Transformer]
graph LR
    DOC["Legal Document\n n >> 4096 tokens"] -->|"Chunk into\n segments of c"| CHUNKS["Segments\n n/c chunks\n each in N^c"]
    CHUNKS -->|"W_emb in R^V x d"| EMB["Segment Emb\n in R^c x d per chunk"]
    EMB --> LOCAL["Local Encoder\n Self-attn per chunk\n O(c^2) memory"]
    LOCAL --> GLOBAL["Global Encoder\n Cross-chunk attn\n summary tokens\n STORED: all activations"]
    GLOBAL -->|"Task head"| OUT["Contract analysis\n Clause classification\n in R^K"]

    style DOC fill:#e8f5e9,stroke:#4caf50,color:#000
    style LOCAL fill:#e3f2fd,stroke:#2196f3,color:#000
    style GLOBAL fill:#fff3e0,stroke:#ff9800,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)

DIAGRAMS["chapter33_observability"] = (
    r"\subsection{Machine Language Grammar}",
    r"""
\begin{mermaid}[ML Observability Architecture]
graph LR
    MODEL["Model\n in Production"] -->|"Inference logs"| METRICS["Metrics Collector\n latency, throughput\n predictions"]
    DATA["Input Data\n Stream"] -->|"Feature stats"| DRIFT["Drift Detector\n Compare P_train vs P_prod\n KL divergence, PSI"]
    METRICS --> DASH["Dashboard\n Alerts on:\n accuracy drop\n latency spike"]
    DRIFT --> DASH
    DASH -->|"Trigger"| RETRAIN["Retrain Pipeline\n Fine-tune on\n new data\n Memory: same as training"]

    style MODEL fill:#e8f5e9,stroke:#4caf50,color:#000
    style DRIFT fill:#fff3e0,stroke:#ff9800,color:#000
    style DASH fill:#e3f2fd,stroke:#2196f3,color:#000
    style RETRAIN fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)

DIAGRAMS["chapter34_dsl_agents"] = (
    r"\section{Designing Domain-Specific Languages}",
    r"""
\begin{mermaid}[LLM Agent Architecture]
graph LR
    USER["User Query\n text input"] --> LLM["LLM Agent\n Decoder-only Transformer\n Context window: n tokens\n STORED: KV cache\n in R^L x 2 x n x d_k\n per layer"]
    LLM -->|"Function call\n (tool selection)"| TOOL["Tool Execution\n Code / Search / API\n External memory"]
    TOOL -->|"Observation\n appended to context"| LLM
    LLM -->|"Reasoning loop\n until done"| OUT["Final Response\n Generated text"]

    LLM -->|"KV Cache grows\n O(n * L * d) memory\n per generation step"| KV["KV Cache\n Inference bottleneck\n Quantize to INT8\n for efficiency"]

    style USER fill:#e8f5e9,stroke:#4caf50,color:#000
    style LLM fill:#fff3e0,stroke:#ff9800,color:#000
    style TOOL fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000
\end{mermaid}

"""
)


def inject_diagram(filepath, search_text, mermaid_block):
    """Insert mermaid_block after the first occurrence of search_text in filepath."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if r'\begin{mermaid}' in content:
        print(f"  SKIP (already has mermaid): {os.path.basename(filepath)}")
        return False

    idx = content.find(search_text)
    if idx == -1:
        # Try with normalized whitespace
        normalized = ' '.join(search_text.split())
        for i in range(len(content) - len(normalized)):
            chunk = ' '.join(content[i:i+len(search_text)+50].split())
            if chunk.startswith(normalized):
                idx = i
                break

    if idx == -1:
        print(f"  FAIL (pattern not found): {os.path.basename(filepath)}")
        print(f"    Pattern: {search_text[:80]}...")
        return None

    # Find end of the line containing the search text
    end_of_line = content.find('\n', idx + len(search_text))
    if end_of_line == -1:
        end_of_line = len(content)

    content = content[:end_of_line] + '\n' + mermaid_block + content[end_of_line:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK: {os.path.basename(filepath)}")
    return True


def main():
    success = 0
    fail = 0
    skip = 0

    for chapter_id, (search_text, mermaid_block) in DIAGRAMS.items():
        filepath = os.path.join(CHAPTERS_DIR, f"{chapter_id}.tex")
        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {filepath}")
            fail += 1
            continue

        result = inject_diagram(filepath, search_text, mermaid_block)
        if result is True:
            success += 1
        elif result is False:
            skip += 1
        else:
            fail += 1

    print(f"\nDone: {success} injected, {skip} skipped, {fail} failed")


if __name__ == "__main__":
    main()
