#!/usr/bin/env python3
"""Replace existing mermaid diagrams in .tex files with improved versions.
Key changes: every input (data, weight, bias) is a SEPARATE box node.
"""
import re, os

CHAPTERS_DIR = "chapters"

# New diagram code (between \begin{mermaid}[caption] and \end{mermaid})
# Use raw strings so \n is literal backslash-n (line breaks in mermaid labels)
NEW = {}

# ── Ch1: Linear Algebra ──────────────────────────────────────────────────────
NEW["chapter01_linear_algebra"] = (
    "Linear Transformation in Neural Networks",
    r"""graph LR
    X["Input x\n in R^n"] --> Z["z = Wx + b\n in R^m\n STORED: x, z"]
    W["Weight W\n in R^m x n"] --> Z
    B["Bias b\n in R^m"] --> Z
    Z -->|"sigma"| H["h = sigma(z)\n in R^m\n STORED: z for sigma'"]

    H -.->|"Backprop needs sigma'(z)"| Z
    Z -.->|"dL/dW = delta * x^T"| W

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style W fill:#fff3e0,stroke:#ff9800,color:#000
    style B fill:#fff3e0,stroke:#ff9800,color:#000
    style Z fill:#e3f2fd,stroke:#2196f3,color:#000
    style H fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch2: Calculus and Optimization ────────────────────────────────────────────
NEW["chapter02_calculus_optimization"] = (
    "Gradient Descent with Backpropagation",
    r"""graph LR
    X["Data batch x\n in R^B x d"] --> FWD["Forward pass\n f(x; theta)\n STORED: all z_l, h_l\n per layer"]
    T["Parameters theta\n in R^p"] --> FWD
    FWD --> L["Loss L(y_hat, y)\n scalar"]
    L --> G["Gradients\n dL/d_theta in R^p\n via chain rule\n Uses stored z_l, h_l"]
    G -->|"theta -= eta * grad"| T

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style T fill:#fff3e0,stroke:#ff9800,color:#000
    style FWD fill:#e3f2fd,stroke:#2196f3,color:#000
    style L fill:#fce4ec,stroke:#e91e63,color:#000
    style G fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch3: Probability and Information Theory ───────────────────────────────────
NEW["chapter03_probability_information"] = (
    "Cross-Entropy Loss in Classification",
    r"""graph LR
    X["Input x\n in R^d"] --> LOGITS["Logits z = Wx + b\n in R^K\n STORED for backprop"]
    W["Weights W\n in R^K x d"] --> LOGITS
    Bb["Bias b\n in R^K"] --> LOGITS
    LOGITS -->|"softmax"| P["Probabilities\n p_k = exp(z_k)/sum\n in R^K\n STORED for gradient"]
    Y["True label y\n one-hot in R^K"] --> CE["Cross-Entropy\n H = -sum(y_k log p_k)\n scalar"]
    P --> CE
    CE -.->|"dL/dz_k = p_k - y_k"| LOGITS

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style W fill:#fff3e0,stroke:#ff9800,color:#000
    style Bb fill:#fff3e0,stroke:#ff9800,color:#000
    style LOGITS fill:#e3f2fd,stroke:#2196f3,color:#000
    style P fill:#e3f2fd,stroke:#2196f3,color:#000
    style CE fill:#fce4ec,stroke:#e91e63,color:#000""")

# ── Ch4: Feed-Forward Networks ────────────────────────────────────────────────
NEW["chapter04_feedforward_networks"] = (
    "MLP Forward and Backward Pass",
    r"""graph LR
    X["Input x\n in R^n0"] --> Z1["z1 = W1*x + b1\n in R^n1\n STORED for backprop"]
    W1["W1\n in R^n1 x n0"] --> Z1
    B1["b1\n in R^n1"] --> Z1
    Z1 -->|"sigma"| H1["h1 = sigma(z1)\n in R^n1\n STORED for backprop"]
    H1 --> Z2["z2 = W2*h1 + b2\n in R^n2\n STORED for backprop"]
    W2["W2\n in R^n2 x n1"] --> Z2
    B2["b2\n in R^n2"] --> Z2
    Z2 -->|"softmax"| Y["y_hat in R^n2"]
    Y --> L["Loss L"]

    L -.->|"dL/dz2"| Z2
    H1 -.->|"dL/dz1"| Z1

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style W1 fill:#fff3e0,stroke:#ff9800,color:#000
    style B1 fill:#fff3e0,stroke:#ff9800,color:#000
    style W2 fill:#fff3e0,stroke:#ff9800,color:#000
    style B2 fill:#fff3e0,stroke:#ff9800,color:#000
    style Z1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style H1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style Z2 fill:#e3f2fd,stroke:#2196f3,color:#000
    style Y fill:#f3e5f5,stroke:#9c27b0,color:#000
    style L fill:#fce4ec,stroke:#e91e63,color:#000""")

# ── Ch5: Convolutional Networks ───────────────────────────────────────────────
NEW["chapter05_convolutional_networks"] = (
    "CNN Forward Pass with Memory",
    r"""graph LR
    X["Input X\n in R^H x W x C_in"] --> CONV["Conv2D Output\n in R^H' x W' x C_out\n STORED: X for dL/dK"]
    K["Filters K\n in R^k x k x C_in x C_out"] --> CONV
    BC["Bias b\n in R^C_out"] --> CONV
    CONV -->|"ReLU"| ACT["ReLU(conv)\n in R^H' x W' x C_out\n STORED for ReLU'"]
    ACT --> POOL["MaxPool\n in R^H'' x W'' x C_out\n STORED: max indices"]
    POOL -->|"Flatten"| FLAT["Flat vector\n in R^D"]
    FLAT --> FC["FC: z = W*flat + b\n in R^K"]
    WFC["W_fc\n in R^K x D"] --> FC
    BFC["b_fc\n in R^K"] --> FC
    FC -->|"softmax"| OUT["y_hat in R^K"]

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style K fill:#fff3e0,stroke:#ff9800,color:#000
    style BC fill:#fff3e0,stroke:#ff9800,color:#000
    style WFC fill:#fff3e0,stroke:#ff9800,color:#000
    style BFC fill:#fff3e0,stroke:#ff9800,color:#000
    style CONV fill:#e3f2fd,stroke:#2196f3,color:#000
    style ACT fill:#e3f2fd,stroke:#2196f3,color:#000
    style POOL fill:#e3f2fd,stroke:#2196f3,color:#000
    style FC fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch6: Recurrent Networks ──────────────────────────────────────────────────
NEW["chapter06_recurrent_networks"] = (
    "RNN/LSTM Forward Pass with Memory",
    r"""graph LR
    subgraph TimeStep["Each Timestep t"]
        XT["Input x_t\n in R^d"] --> Z["z_t\n in R^h\n STORED for tanh'"]
        HTP["Hidden h_t-1\n in R^h"] --> Z
        Wxh["W_xh\n in R^h x d"] --> Z
        Whh["W_hh\n in R^h x h"] --> Z
        Bh["b_h\n in R^h"] --> Z
        Z -->|"tanh"| HT["h_t = tanh(z_t)\n in R^h\n STORED: h_t-1, x_t"]
        HT --> YT["y_t in R^k"]
        Why["W_hy\n in R^k x h"] --> YT
        By["b_y\n in R^k"] --> YT
    end

    subgraph LSTM["LSTM Gating"]
        FG["Forget f_t = sigma(W_f*[h,x])\n in R^h -- STORED"]
        IG["Input i_t = sigma(W_i*[h,x])\n in R^h -- STORED"]
        CS["Cell c_t = f*c + i*c~\n in R^h -- STORED"]
    end

    style XT fill:#e8f5e9,stroke:#4caf50,color:#000
    style HTP fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wxh fill:#fff3e0,stroke:#ff9800,color:#000
    style Whh fill:#fff3e0,stroke:#ff9800,color:#000
    style Bh fill:#fff3e0,stroke:#ff9800,color:#000
    style Why fill:#fff3e0,stroke:#ff9800,color:#000
    style By fill:#fff3e0,stroke:#ff9800,color:#000
    style Z fill:#e3f2fd,stroke:#2196f3,color:#000
    style HT fill:#e3f2fd,stroke:#2196f3,color:#000
    style YT fill:#f3e5f5,stroke:#9c27b0,color:#000
    style CS fill:#fce4ec,stroke:#e91e63,color:#000""")

# ── Ch7: Attention Fundamentals ──────────────────────────────────────────────
NEW["chapter07_attention_fundamentals"] = (
    "Scaled Dot-Product Attention Data Flow",
    r"""graph LR
    Q["Queries Q\n in R^m x d_k"] --> S["Scores\n E = Q * K^T\n in R^m x n\n STORED for backprop"]
    K["Keys K\n in R^n x d_k"] --> S
    S -->|"/ sqrt(d_k)"| SC["Scaled Scores\n E / sqrt(d_k)\n in R^m x n"]
    SC -->|"softmax row-wise"| A["Attn Weights A\n in R^m x n\n STORED for dL/dV"]
    A --> OUT["Output A*V\n in R^m x d_v\n STORED: A, V"]
    V["Values V\n in R^n x d_v"] --> OUT

    style Q fill:#e3f2fd,stroke:#2196f3,color:#000
    style K fill:#e8f5e9,stroke:#4caf50,color:#000
    style V fill:#fff3e0,stroke:#ff9800,color:#000
    style S fill:#e3f2fd,stroke:#2196f3,color:#000
    style A fill:#f3e5f5,stroke:#9c27b0,color:#000
    style OUT fill:#fce4ec,stroke:#e91e63,color:#000""")

# ── Ch8: Self-Attention and Multi-Head ────────────────────────────────────────
NEW["chapter08_self_attention"] = (
    "Multi-Head Self-Attention Data Flow",
    r"""graph LR
    X["Input X\n in R^n x d_model"] --> Q["Q_i = X*W_Q\n in R^n x d_k"]
    WQ["W_Q^i\n in R^d_model x d_k\n per head"] --> Q
    X --> KK["K_i = X*W_K\n in R^n x d_k"]
    WK["W_K^i\n in R^d_model x d_k"] --> KK
    X --> V["V_i = X*W_V\n in R^n x d_v"]
    WV["W_V^i\n in R^d_model x d_v"] --> V
    Q --> ATT["Attention\n softmax(QK^T/sqrt(d_k))*V\n h heads in parallel\n STORED: attn weights"]
    KK --> ATT
    V --> ATT
    ATT -->|"Concat heads"| CAT["Concat\n in R^n x h*d_v"]
    CAT --> OUT["Output\n in R^n x d_model"]
    WO["W_O\n in R^h*d_v x d_model"] --> OUT

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style WQ fill:#fff3e0,stroke:#ff9800,color:#000
    style WK fill:#fff3e0,stroke:#ff9800,color:#000
    style WV fill:#fff3e0,stroke:#ff9800,color:#000
    style WO fill:#fff3e0,stroke:#ff9800,color:#000
    style Q fill:#e3f2fd,stroke:#2196f3,color:#000
    style KK fill:#e3f2fd,stroke:#2196f3,color:#000
    style V fill:#e3f2fd,stroke:#2196f3,color:#000
    style ATT fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch9: Attention Variants ──────────────────────────────────────────────────
NEW["chapter09_attention_variants"] = (
    "Cross-Attention vs Self-Attention Data Flow",
    r"""graph LR
    subgraph SelfAttn["Self-Attention"]
        SX["X in R^n x d"] --> SQ["Q from X"]
        SX --> SK["K from X"]
        SX --> SV["V from X"]
        SWQ["W_Q"] --> SQ
        SWK["W_K"] --> SK
        SWV["W_V"] --> SV
        SQ --> SOUT["Output in R^n x d\n Memory: O(n^2)"]
        SK --> SOUT
        SV --> SOUT
    end

    subgraph CrossAttn["Cross-Attention"]
        DX["Decoder X_dec\n in R^m x d"] --> CQ["Q = X_dec*W_Q\n in R^m x d_k"]
        CWQ["W_Q\n in R^d x d_k"] --> CQ
        EX["Encoder X_enc\n in R^n x d"] --> CK["K in R^n x d_k"]
        EX --> CV["V in R^n x d_v"]
        CWK["W_K\n in R^d x d_k"] --> CK
        CWV["W_V\n in R^d x d_v"] --> CV
        CQ --> COUT["Output in R^m x d_v\n Memory: O(m*n)"]
        CK --> COUT
        CV --> COUT
    end

    style SX fill:#e8f5e9,stroke:#4caf50,color:#000
    style DX fill:#e3f2fd,stroke:#2196f3,color:#000
    style EX fill:#e8f5e9,stroke:#4caf50,color:#000
    style SWQ fill:#fff3e0,stroke:#ff9800,color:#000
    style SWK fill:#fff3e0,stroke:#ff9800,color:#000
    style SWV fill:#fff3e0,stroke:#ff9800,color:#000
    style CWQ fill:#fff3e0,stroke:#ff9800,color:#000
    style CWK fill:#fff3e0,stroke:#ff9800,color:#000
    style CWV fill:#fff3e0,stroke:#ff9800,color:#000
    style COUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch10: Transformer Model ──────────────────────────────────────────────────
NEW["chapter10_transformer_model"] = (
    "Transformer Encoder Layer Forward Pass",
    r"""graph LR
    X["Input X\n in R^n x d_model"] --> MHA["Multi-Head\n Self-Attention\n STORED: Q,K,V,\n attn weights"]
    MHA --> ADD1["Residual\n X + MHA(X)"]
    ADD1 --> LN1["LayerNorm\n in R^n x d_model\n STORED: mean, var"]
    LN1 --> FFN1["ReLU(W1*x + b1)\n in R^n x d_ff\n STORED: pre-ReLU"]
    W1["W1\n in R^d_model x d_ff"] --> FFN1
    B1ff["b1\n in R^d_ff"] --> FFN1
    FFN1 --> FFN2["W2*h + b2\n in R^n x d_model\n STORED: h for dL/dW2"]
    W2["W2\n in R^d_ff x d_model"] --> FFN2
    B2ff["b2\n in R^d_model"] --> FFN2
    FFN2 --> ADD2["Residual\n LN1 + FFN"]
    ADD2 --> LN2["LayerNorm Output\n in R^n x d_model"]

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style MHA fill:#e3f2fd,stroke:#2196f3,color:#000
    style W1 fill:#fff3e0,stroke:#ff9800,color:#000
    style B1ff fill:#fff3e0,stroke:#ff9800,color:#000
    style W2 fill:#fff3e0,stroke:#ff9800,color:#000
    style B2ff fill:#fff3e0,stroke:#ff9800,color:#000
    style FFN1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style FFN2 fill:#e3f2fd,stroke:#2196f3,color:#000
    style LN2 fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch11: Training Transformers ──────────────────────────────────────────────
NEW["chapter11_training_transformers"] = (
    "Transformer Training Pipeline",
    r"""graph LR
    D["Raw Text"] -->|"BPE/WordPiece"| TOK["Token IDs\n in N^B x n"]
    TOK --> EMB["Token Embeddings\n in R^B x n x d\n STORED for backprop"]
    Wemb["W_emb\n in R^V x d"] --> EMB
    Wpos["W_pos / sinusoidal\n in R^n_max x d"] --> EMB
    EMB --> TF["Transformer\n Layers x L\n STORED per layer:\n activations, attn"]
    TF --> LM["LM Head logits\n in R^B x n x V\n STORED for softmax"]
    Whead["W_head\n in R^d x V"] --> LM
    LM -->|"Cross-Entropy"| LOSS["Loss"]
    LOSS -.->|"Backward: O(L*n*d + n^2*h)"| TF
    LOSS -.->|"AdamW: 2x param memory"| OPT["Optimizer step"]

    style D fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wemb fill:#fff3e0,stroke:#ff9800,color:#000
    style Wpos fill:#fff3e0,stroke:#ff9800,color:#000
    style Whead fill:#fff3e0,stroke:#ff9800,color:#000
    style TF fill:#e3f2fd,stroke:#2196f3,color:#000
    style LM fill:#e3f2fd,stroke:#2196f3,color:#000
    style LOSS fill:#fce4ec,stroke:#e91e63,color:#000
    style OPT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch12: Computational Analysis ─────────────────────────────────────────────
NEW["chapter12_computational_analysis"] = (
    "Transformer Computation and Memory per Layer",
    r"""graph LR
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
    style WM fill:#fff3e0,stroke:#ff9800,color:#000
    style ACT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch13: BERT ───────────────────────────────────────────────────────────────
NEW["chapter13_bert"] = (
    "BERT Architecture Data Flow",
    r"""graph LR
    TOK["Token IDs\n [CLS] t1 [MASK] t3 [SEP]\n in N^n"] --> TE["Token Emb\n in R^n x d"]
    Wtok["W_tok\n in R^V x d"] --> TE
    SEG["Segment IDs\n in {0,1}^n"] --> SE["Seg Emb\n in R^n x d"]
    Wseg["W_seg\n in R^2 x d"] --> SE
    POS["Position 0..n-1"] --> PE["Pos Emb\n in R^n x d"]
    Wpos["W_pos\n in R^n_max x d"] --> PE

    TE --> ADD["Sum Embeddings\n E = Tok + Seg + Pos\n in R^n x d\n STORED for backprop"]
    SE --> ADD
    PE --> ADD

    ADD --> ENC["Transformer Encoder\n x L layers (12/24)\n MHA + FFN + LN\n STORED per layer"]

    ENC --> CLS["CLS output --> NSP\n in R^d"]
    Wnsp["W_nsp\n in R^d x 2"] --> CLS
    ENC --> MLM["Masked --> MLM head\n in R^k x d"]
    Wmlm["W_mlm\n in R^d x V"] --> MLM

    style TOK fill:#e8f5e9,stroke:#4caf50,color:#000
    style SEG fill:#e8f5e9,stroke:#4caf50,color:#000
    style POS fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wtok fill:#fff3e0,stroke:#ff9800,color:#000
    style Wseg fill:#fff3e0,stroke:#ff9800,color:#000
    style Wpos fill:#fff3e0,stroke:#ff9800,color:#000
    style Wnsp fill:#fff3e0,stroke:#ff9800,color:#000
    style Wmlm fill:#fff3e0,stroke:#ff9800,color:#000
    style ADD fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style CLS fill:#f3e5f5,stroke:#9c27b0,color:#000
    style MLM fill:#fce4ec,stroke:#e91e63,color:#000""")

# ── Ch14: GPT ────────────────────────────────────────────────────────────────
NEW["chapter14_gpt"] = (
    "GPT Decoder-Only Architecture",
    r"""graph LR
    TOK["Input tokens\n x_1..x_t\n in N^t"] --> EMB["Token + Pos Emb\n in R^t x d\n STORED for backprop"]
    Wemb["W_emb\n in R^V x d"] --> EMB
    Wpos["W_pos\n in R^n_max x d"] --> EMB
    EMB --> DEC["Decoder x L layers\n 1. Masked Self-Attn\n (causal mask)\n STORED: Q,K,V,attn\n 2. FFN\n STORED: activations"]
    DEC --> LM["LM Head logits\n in R^t x V"]
    Whead["W_head\n in R^d x V\n (tied with W_emb)"] --> LM
    LM -->|"softmax"| PRED["P(x_t+1 | x_1..x_t)\n in R^V"]

    PRED -.->|"Backprop: O(L*t*d + L*t^2)"| EMB

    style TOK fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wemb fill:#fff3e0,stroke:#ff9800,color:#000
    style Wpos fill:#fff3e0,stroke:#ff9800,color:#000
    style Whead fill:#fff3e0,stroke:#ff9800,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style DEC fill:#e3f2fd,stroke:#2196f3,color:#000
    style LM fill:#e3f2fd,stroke:#2196f3,color:#000
    style PRED fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch15: T5 and BART ────────────────────────────────────────────────────────
NEW["chapter15_t5_bart"] = (
    "T5 Encoder-Decoder Architecture",
    r"""graph LR
    SRC["Source tokens\n in N^n"] --> EEMB["Encoder Emb\n in R^n x d"]
    Wemb["Shared W_emb\n in R^V x d"] --> EEMB
    RelP["Relative Pos Bias"] --> EEMB
    EEMB --> ENC["Encoder x L layers\n Self-Attn + FFN\n STORED: all activations\n Output in R^n x d"]

    TGT["Target tokens\n in N^m"] --> DEMB["Decoder Emb\n in R^m x d"]
    Wemb --> DEMB
    DEMB --> DSAL["Decoder x L layers\n 1. Causal Self-Attn\n 2. Cross-Attn to Enc\n 3. FFN\n STORED: Q,K,V per layer"]
    ENC --> DSAL

    DSAL --> OUT["Output logits\n in R^m x V"]
    Whead["W_head\n in R^d x V"] --> OUT

    style SRC fill:#e8f5e9,stroke:#4caf50,color:#000
    style TGT fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wemb fill:#fff3e0,stroke:#ff9800,color:#000
    style Whead fill:#fff3e0,stroke:#ff9800,color:#000
    style ENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style DSAL fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch16: Efficient Transformers ─────────────────────────────────────────────
NEW["chapter16_efficient_transformers"] = (
    "Efficient Attention Approaches and Memory",
    r"""graph LR
    Q["Query Q\n in R^n x d"] --> FULL["Full Attention\n softmax(QK^T/sqrt(d))V\n Compute: O(n^2 d)\n Memory: O(n^2)"]
    K["Key K\n in R^n x d"] --> FULL
    V["Value V\n in R^n x d"] --> FULL

    FULL --> SPARSE["Sparse Attention\n Subset of n^2 entries\n Memory: O(n * w)\n w = window size"]
    FULL --> LINEAR["Linear Attention\n phi(Q)*[phi(K)^T*V]\n Compute: O(n * d^2)\n Memory: O(n * d)"]
    FULL --> FLASH["FlashAttention\n Tiled computation\n Recompute in backward\n Peak memory: O(n)"]

    style Q fill:#e8f5e9,stroke:#4caf50,color:#000
    style K fill:#e8f5e9,stroke:#4caf50,color:#000
    style V fill:#e8f5e9,stroke:#4caf50,color:#000
    style FULL fill:#fce4ec,stroke:#e91e63,color:#000
    style SPARSE fill:#e3f2fd,stroke:#2196f3,color:#000
    style LINEAR fill:#e8f5e9,stroke:#4caf50,color:#000
    style FLASH fill:#fff3e0,stroke:#ff9800,color:#000""")

# ── Ch17: Vision Transformers ────────────────────────────────────────────────
NEW["chapter17_vision_transformers"] = (
    "Vision Transformer (ViT) Forward Pass",
    r"""graph LR
    IMG["Image I\n in R^H x W x C"] -->|"Split P x P patches"| PAT["N = HW/P^2 patches\n each in R^(P^2*C)"]
    PAT --> EMB["Patch Embeddings\n in R^N x d\n STORED for backprop"]
    Wpatch["W_patch\n in R^(P^2*C) x d"] --> EMB
    Bpatch["b_patch\n in R^d"] --> EMB
    CLS["[CLS] token\n learnable in R^d"] --> CAT["Prepend [CLS]\n in R^(N+1) x d"]
    EMB --> CAT
    POS["Position Emb\n E_pos in R^(N+1) x d"] --> ADD["Add Pos Emb"]
    CAT --> ADD
    ADD --> ENC["Transformer Encoder\n x L layers\n STORED: activations\n Memory: O(L*(N+1)^2)"]
    ENC --> HEAD["MLP Head\n Output in R^K"]
    Whead["W_head\n in R^d x K"] --> HEAD

    style IMG fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wpatch fill:#fff3e0,stroke:#ff9800,color:#000
    style Bpatch fill:#fff3e0,stroke:#ff9800,color:#000
    style CLS fill:#fff3e0,stroke:#ff9800,color:#000
    style POS fill:#fff3e0,stroke:#ff9800,color:#000
    style Whead fill:#fff3e0,stroke:#ff9800,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style HEAD fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch18: Multimodal Transformers ────────────────────────────────────────────
NEW["chapter18_multimodal_transformers"] = (
    "Multimodal Transformer Fusion",
    r"""graph LR
    TXT["Text tokens\n in N^n_t"] --> TE["Text Emb\n in R^n_t x d"]
    Wtext["W_text\n in R^V x d"] --> TE
    IMG["Image patches\n in R^N x (P^2*C)"] --> IE["Image Emb\n in R^N x d"]
    Wimg["W_img\n in R^(P^2*C) x d"] --> IE

    TE --> FUSE["Concatenate\n [text; image]\n in R^(n_t+N) x d"]
    IE --> FUSE
    FUSE --> ENC["Joint Transformer\n x L layers\n Cross-modal attention\n STORED: all activations\n Memory: O(L*(n_t+N)^2)"]
    ENC --> TOUT["Text output in R^n_t x d"]
    ENC --> IOUT["Image output in R^N x d"]

    style TXT fill:#e8f5e9,stroke:#4caf50,color:#000
    style IMG fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wtext fill:#fff3e0,stroke:#ff9800,color:#000
    style Wimg fill:#fff3e0,stroke:#ff9800,color:#000
    style FUSE fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style TOUT fill:#f3e5f5,stroke:#9c27b0,color:#000
    style IOUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch19: Long Context ───────────────────────────────────────────────────────
NEW["chapter19_long_context"] = (
    "Long Context Attention Strategies",
    r"""graph LR
    SEQ["Long sequence\n n >> 4096 tokens\n Full attn: O(n^2)"]

    SEQ --> SW["Sliding Window\n w neighbors each side\n Memory: O(n*w)\n STORED: local attn only"]
    SEQ --> CHUNK["Chunked Attention\n n/c chunks of size c\n Intra: O(c^2)\n Cross: summary tokens"]
    SEQ --> ROPE["RoPE Scaling\n Rotary Pos Emb\n Extend via interpolation\n No extra memory"]

    style SEQ fill:#fce4ec,stroke:#e91e63,color:#000
    style SW fill:#e3f2fd,stroke:#2196f3,color:#000
    style CHUNK fill:#e8f5e9,stroke:#4caf50,color:#000
    style ROPE fill:#fff3e0,stroke:#ff9800,color:#000""")

# ── Ch20: Pretraining Strategies ─────────────────────────────────────────────
NEW["chapter20_pretraining_strategies"] = (
    "Pre-training Objectives Comparison",
    r"""graph LR
    subgraph CLM["Causal LM (GPT)"]
        C1["x_1..x_t"] --> C2["Predict x_t+1\n Causal mask\n Memory: O(t^2)"]
    end

    subgraph MLM_["Masked LM (BERT)"]
        M1["x with [MASK]"] --> M2["Predict masked\n Bidirectional\n Memory: O(n^2)"]
    end

    subgraph S2S["Seq2Seq (T5)"]
        S1["Corrupted input"] --> S2["Encoder repr\n in R^n x d"]
        S2 --> S3["Decode spans\n Cross-attn: O(m*n)"]
    end

    style C2 fill:#e3f2fd,stroke:#2196f3,color:#000
    style M2 fill:#e8f5e9,stroke:#4caf50,color:#000
    style S3 fill:#fff3e0,stroke:#ff9800,color:#000""")

# ── Ch21: PyTorch Implementation ─────────────────────────────────────────────
NEW["chapter21_pytorch_implementation"] = (
    "PyTorch Transformer Module Hierarchy",
    r"""graph LR
    TF["Transformer\n nn.Module"] --> ENC["Encoder\n N x EncoderLayer"]
    TF --> DEC["Decoder\n N x DecoderLayer"]
    EMB_M["nn.Embedding\n V x d params"] --> TF
    HEAD_M["nn.Linear\n d x V params"] --> TF

    ENC --> ELYR["EncoderLayer"]
    MHA_M["MultiHeadAttn\n W_Q,W_K,W_V,W_O\n params: 4*d^2"] --> ELYR
    FFN_M["FFN\n W1: d*4d, W2: 4d*d\n params: 8*d^2"] --> ELYR
    LN_M["LayerNorm\n gamma, beta: 2*d"] --> ELYR

    DEC --> DLYR["DecoderLayer\n Masked Self-Attn\n + Cross-Attn + FFN"]

    style TF fill:#e8f5e9,stroke:#4caf50,color:#000
    style EMB_M fill:#fff3e0,stroke:#ff9800,color:#000
    style HEAD_M fill:#fff3e0,stroke:#ff9800,color:#000
    style MHA_M fill:#fff3e0,stroke:#ff9800,color:#000
    style FFN_M fill:#fff3e0,stroke:#ff9800,color:#000
    style LN_M fill:#fff3e0,stroke:#ff9800,color:#000
    style ELYR fill:#e3f2fd,stroke:#2196f3,color:#000
    style DLYR fill:#e3f2fd,stroke:#2196f3,color:#000""")

# ── Ch22: Hardware Optimization ──────────────────────────────────────────────
NEW["chapter22_hardware_optimization"] = (
    "GPU Memory Hierarchy and Optimization",
    r"""graph LR
    PARAM["Model Params\n W in R^P\n FP16: 2P bytes"] --> HBM["HBM (GPU RAM)\n 40-80 GB\n BW: 2 TB/s"]
    GRAD["Gradients\n in R^P\n FP16: 2P bytes"] --> HBM
    OPT_S["Optimizer States\n m_t, v_t in R^P\n FP32: 8P bytes"] --> HBM
    ACT_M["Activations\n O(L*n*d)\n for backprop"] --> HBM
    HBM --> SRAM["SRAM On-chip\n ~20 MB/SM\n BW: 19 TB/s\n FlashAttn tiles"]

    subgraph Optim["Optimizations"]
        MP["Mixed Precision\n FP16 fwd/bwd\n Saves ~50%"]
        GC["Grad Checkpoint\n Recompute acts\n +33% compute"]
        FSDP["FSDP/ZeRO\n Shard across N GPUs\n O(P/N) per GPU"]
    end

    HBM --> Optim

    style PARAM fill:#e8f5e9,stroke:#4caf50,color:#000
    style GRAD fill:#e8f5e9,stroke:#4caf50,color:#000
    style OPT_S fill:#fff3e0,stroke:#ff9800,color:#000
    style ACT_M fill:#fff3e0,stroke:#ff9800,color:#000
    style HBM fill:#e3f2fd,stroke:#2196f3,color:#000
    style SRAM fill:#e3f2fd,stroke:#2196f3,color:#000
    style GC fill:#fce4ec,stroke:#e91e63,color:#000""")

# ── Ch23: Best Practices ────────────────────────────────────────────────────
NEW["chapter23_best_practices"] = (
    "Model Development Pipeline",
    r"""graph LR
    DATA["Training Data"] --> TOK["Tokenize\n Vocab V"]
    TOK --> BASE["Baseline Model\n small config"]
    BASE -->|"Scale up"| TRAIN["Full Training\n Memory budget:\n Params: 2P (FP16)\n Grads: 2P\n Adam: 8P\n Acts: O(L*n*d)"]
    LR["Hyperparams\n lr, warmup, wd"] --> TRAIN
    TRAIN --> EVAL["Evaluate\n Loss, Perplexity"]
    EVAL -->|"Tune"| LR

    style DATA fill:#e8f5e9,stroke:#4caf50,color:#000
    style LR fill:#fff3e0,stroke:#ff9800,color:#000
    style TRAIN fill:#e3f2fd,stroke:#2196f3,color:#000
    style EVAL fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch24: Domain-Specific Models ─────────────────────────────────────────────
NEW["chapter24_domain_specific_models"] = (
    "Domain Adaptation Pipeline",
    r"""graph LR
    BASE["Pre-trained LM\n params in R^P"] --> DAPT["Domain-Adaptive\n Pre-training\n on domain text"]
    CORPUS["Domain Corpus"] --> DAPT
    DAPT --> FT["Fine-tuning\n on task data"]
    TASK["Task Data\n labeled"] --> FT
    Wtask["W_task\n in R^d x K"] --> FT
    FT --> DEPLOY["Domain Model\n BioBERT / LegalBERT"]

    style BASE fill:#e8f5e9,stroke:#4caf50,color:#000
    style CORPUS fill:#e8f5e9,stroke:#4caf50,color:#000
    style TASK fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wtask fill:#fff3e0,stroke:#ff9800,color:#000
    style DAPT fill:#e3f2fd,stroke:#2196f3,color:#000
    style FT fill:#e3f2fd,stroke:#2196f3,color:#000
    style DEPLOY fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch25: Enterprise NLP ─────────────────────────────────────────────────────
NEW["chapter25_enterprise_nlp"] = (
    "RAG Pipeline Architecture",
    r"""graph LR
    Q["Query text"] --> QE["Query Emb\n in R^d"]
    Wenc["Encoder W\n in R^V x d"] --> QE
    DOCS["Document Store\n N docs"] --> DE["Doc Embs\n in R^N x d\n Pre-computed"]
    Wenc --> DE
    QE --> RET["Top-K Retrieval\n cos(q, d_i)\n K docs"]
    DE --> RET
    RET --> GEN["Generator LLM\n Context = query + K docs\n Memory: O((n_q+K*n_d)^2)"]
    GEN --> ANS["Answer text"]

    style Q fill:#e8f5e9,stroke:#4caf50,color:#000
    style DOCS fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wenc fill:#fff3e0,stroke:#ff9800,color:#000
    style RET fill:#e3f2fd,stroke:#2196f3,color:#000
    style GEN fill:#e3f2fd,stroke:#2196f3,color:#000
    style ANS fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch26: Code Language ──────────────────────────────────────────────────────
NEW["chapter26_code_language"] = (
    "Code Language Model Architecture",
    r"""graph LR
    CODE["Source Code\n raw text"] -->|"BPE V=32K-50K"| TOK["Code Tokens\n in N^n"]
    TOK --> EMB["Embeddings\n in R^n x d"]
    Wemb["W_emb\n in R^V x d"] --> EMB
    Wpos["Pos Enc"] --> EMB
    EMB --> DEC["Decoder Layers x L\n Causal Self-Attn + FFN\n STORED: activations"]
    DEC --> OUT["Logits in R^n x V"]
    Whead["W_head\n in R^d x V"] --> OUT

    style CODE fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wemb fill:#fff3e0,stroke:#ff9800,color:#000
    style Wpos fill:#fff3e0,stroke:#ff9800,color:#000
    style Whead fill:#fff3e0,stroke:#ff9800,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style DEC fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch27: Video Visual ───────────────────────────────────────────────────────
NEW["chapter27_video_visual"] = (
    "Video Transformer Architecture",
    r"""graph LR
    VID["Video\n T x H x W x C"] -->|"P x P patches"| PAT["T*N patches\n each in R^(P^2*C)"]
    PAT --> EMB["Space-Time Emb\n in R^(T*N) x d"]
    Wpatch["W_patch\n in R^(P^2*C) x d"] --> EMB
    Tpos["Temporal Pos Enc"] --> EMB
    EMB --> SENC["Spatial Encoder\n per-frame self-attn\n O(N^2) per frame"]
    SENC --> TENC["Temporal Encoder\n cross-frame attn\n O(T^2) per position"]
    TENC --> OUT["Video repr\n in R^(T*N) x d"]

    style VID fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wpatch fill:#fff3e0,stroke:#ff9800,color:#000
    style Tpos fill:#fff3e0,stroke:#ff9800,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style SENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style TENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch28: Knowledge Graphs ───────────────────────────────────────────────────
NEW["chapter28_knowledge_graphs"] = (
    "Knowledge-Enhanced Transformer",
    r"""graph LR
    TXT["Text input\n tokens in N^n"] --> TE["Text Emb\n in R^n x d"]
    Wemb["W_emb\n in R^V x d"] --> TE
    KG["Knowledge Graph\n entities + relations"] --> KE["Entity Emb\n in R^k x d"]
    Went["W_ent\n in R^E x d"] --> KE

    TE --> FUSE["Knowledge Fusion\n at linked positions\n in R^n x d"]
    KE --> FUSE
    FUSE --> ENC["Transformer Encoder\n x L layers\n STORED: activations"]
    ENC --> OUT["Enhanced repr\n in R^n x d"]

    style TXT fill:#e8f5e9,stroke:#4caf50,color:#000
    style KG fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wemb fill:#fff3e0,stroke:#ff9800,color:#000
    style Went fill:#fff3e0,stroke:#ff9800,color:#000
    style FUSE fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch29: Recommendations ───────────────────────────────────────────────────
NEW["chapter29_recommendations"] = (
    "Sequential Recommendation Transformer",
    r"""graph LR
    HIST["User history\n item_1..item_t\n in N^t"] --> EMB["Item Emb\n in R^t x d"]
    Witem["W_item\n in R^I x d"] --> EMB
    Wpos["W_pos\n in R^n x d"] --> EMB
    EMB --> ENC["Transformer Encoder\n Causal self-attn x L\n STORED: attn per layer"]
    ENC --> REP["User repr\n in R^d"]
    REP --> SCORE["Scores = repr * W_item^T\n in R^I"]
    Witem --> SCORE
    SCORE -->|"softmax"| TOP["Top-K items"]

    style HIST fill:#e8f5e9,stroke:#4caf50,color:#000
    style Witem fill:#fff3e0,stroke:#ff9800,color:#000
    style Wpos fill:#fff3e0,stroke:#ff9800,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style TOP fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch30: Healthcare ─────────────────────────────────────────────────────────
NEW["chapter30_healthcare"] = (
    "Clinical NLP Pipeline",
    r"""graph LR
    EHR["Clinical Notes\n free text"] -->|"De-identify"| CLEAN["Clean text"]
    CLEAN -->|"Tokenize"| TOK["Tokens in N^n"]
    TOK --> MODEL["ClinicalBERT Encoder\n x L layers\n Pre-trained on MIMIC"]
    Wbert["BERT weights\n domain pre-trained"] --> MODEL
    MODEL --> OUT["NER / Diagnosis"]
    Wtask["Task head W\n in R^d x K"] --> OUT

    style EHR fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wbert fill:#fff3e0,stroke:#ff9800,color:#000
    style Wtask fill:#fff3e0,stroke:#ff9800,color:#000
    style MODEL fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch31: Finance ────────────────────────────────────────────────────────────
NEW["chapter31_finance"] = (
    "Financial Time Series Transformer",
    r"""graph LR
    TS["Price/Volume\n x_1..x_T\n in R^T x F"] --> TEMB["Temporal Emb\n in R^T x d"]
    Wproj["W_proj\n in R^F x d"] --> TEMB
    Tpos["Time Pos Enc"] --> TEMB
    NEWS["News tokens\n in N^n"] --> NE["News Emb\n in R^n x d"]
    Wemb["W_emb\n in R^V x d"] --> NE
    TEMB --> CROSS["Cross-modal Attn\n Memory: O(T*n)"]
    NE --> CROSS
    CROSS --> PRED["Prediction"]
    Wpred["W_pred\n in R^d x 1"] --> PRED

    style TS fill:#e8f5e9,stroke:#4caf50,color:#000
    style NEWS fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wproj fill:#fff3e0,stroke:#ff9800,color:#000
    style Wemb fill:#fff3e0,stroke:#ff9800,color:#000
    style Wpred fill:#fff3e0,stroke:#ff9800,color:#000
    style TEMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style CROSS fill:#e3f2fd,stroke:#2196f3,color:#000
    style PRED fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch32: Legal ──────────────────────────────────────────────────────────────
NEW["chapter32_legal"] = (
    "Legal Document Transformer",
    r"""graph LR
    DOC["Legal Document\n n >> 4096 tokens"] -->|"Chunk"| CHUNKS["Segments\n n/c chunks in N^c"]
    CHUNKS --> EMB["Segment Emb\n in R^c x d"]
    Wemb["W_emb\n in R^V x d"] --> EMB
    EMB --> LOCAL["Local Encoder\n Self-attn per chunk\n O(c^2) memory"]
    LOCAL --> GLOBAL["Global Encoder\n Cross-chunk attn\n STORED: activations"]
    GLOBAL --> OUT["Clause classification\n in R^K"]
    Wtask["Task head W\n in R^d x K"] --> OUT

    style DOC fill:#e8f5e9,stroke:#4caf50,color:#000
    style Wemb fill:#fff3e0,stroke:#ff9800,color:#000
    style Wtask fill:#fff3e0,stroke:#ff9800,color:#000
    style EMB fill:#e3f2fd,stroke:#2196f3,color:#000
    style LOCAL fill:#e3f2fd,stroke:#2196f3,color:#000
    style GLOBAL fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch33: Observability ──────────────────────────────────────────────────────
NEW["chapter33_observability"] = (
    "ML Observability Architecture",
    r"""graph LR
    MODEL["Model in Production"] --> METRICS["Metrics Collector\n latency, throughput"]
    DATA["Input Data Stream"] --> DRIFT["Drift Detector\n P_train vs P_prod\n KL divergence"]
    REF["Training Distribution\n reference stats"] --> DRIFT
    METRICS --> DASH["Dashboard\n Alerts on:\n accuracy drop\n latency spike"]
    DRIFT --> DASH
    DASH -->|"Trigger"| RETRAIN["Retrain Pipeline"]
    NEWDATA["New labeled data"] --> RETRAIN

    style MODEL fill:#e8f5e9,stroke:#4caf50,color:#000
    style DATA fill:#e8f5e9,stroke:#4caf50,color:#000
    style REF fill:#fff3e0,stroke:#ff9800,color:#000
    style NEWDATA fill:#fff3e0,stroke:#ff9800,color:#000
    style DRIFT fill:#e3f2fd,stroke:#2196f3,color:#000
    style DASH fill:#e3f2fd,stroke:#2196f3,color:#000
    style RETRAIN fill:#f3e5f5,stroke:#9c27b0,color:#000""")

# ── Ch34: DSL and Agents ─────────────────────────────────────────────────────
NEW["chapter34_dsl_agents"] = (
    "LLM Agent Architecture",
    r"""graph LR
    USER["User Query"] --> LLM["LLM Agent\n Decoder Transformer\n Context: n tokens"]
    SYSP["System Prompt\n + Tools schema"] --> LLM
    KV["KV Cache\n in R^L x 2 x n x d_k\n grows per step\n O(n*L*d) memory"] --> LLM
    LLM -->|"Tool call"| TOOL["Tool Execution\n Code / Search / API"]
    TOOL -->|"Observation"| LLM
    LLM --> OUT["Final Response"]

    style USER fill:#e8f5e9,stroke:#4caf50,color:#000
    style SYSP fill:#e8f5e9,stroke:#4caf50,color:#000
    style KV fill:#fff3e0,stroke:#ff9800,color:#000
    style LLM fill:#e3f2fd,stroke:#2196f3,color:#000
    style TOOL fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""")


def replace_mermaid_in_file(filepath, caption, code):
    """Replace existing mermaid block in a .tex file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match existing \begin{mermaid}[...]...\end{mermaid}
    pattern = r'\\begin\{mermaid\}\[[^\]]*\].*?\\end\{mermaid\}'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print(f"  NO MERMAID FOUND: {os.path.basename(filepath)}")
        return False

    new_block = f"\\begin{{mermaid}}[{caption}]\n{code}\n\\end{{mermaid}}"
    content = content[:match.start()] + new_block + content[match.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK: {os.path.basename(filepath)}")
    return True


def main():
    ok = 0
    fail = 0
    for chapter_id, (caption, code) in NEW.items():
        filepath = os.path.join(CHAPTERS_DIR, f"{chapter_id}.tex")
        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {filepath}")
            fail += 1
            continue
        if replace_mermaid_in_file(filepath, caption, code):
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} replaced, {fail} failed")


if __name__ == "__main__":
    main()
