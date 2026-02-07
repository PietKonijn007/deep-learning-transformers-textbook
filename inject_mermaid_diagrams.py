#!/usr/bin/env python3
"""
Injects Mermaid.js architecture diagrams into each chapter HTML file.
Places a diagram after the Learning Objectives section in each chapter.
"""

import re
import os

CHAPTERS_DIR = "nodejs-version/public/chapters/deeptech"

# Mapping of chapter filename (without .html) -> (diagram_title, mermaid_code, caption)
DIAGRAMS = {
    "chapter01_linear_algebra": (
        "Linear Transformations in Deep Learning",
        """graph LR
    A["Input Vector<br/>x ∈ ℝⁿ"] --> B["Linear Map<br/>W·x + b"]
    B --> C["Output Vector<br/>y ∈ ℝᵐ"]

    D["Matrix W<br/>ℝᵐˣⁿ"] --> B
    E["Bias b<br/>ℝᵐ"] --> B

    C --> F["Composition<br/>W₂·(W₁·x + b₁) + b₂"]
    F --> G["Deep Network<br/>Layer-by-layer<br/>transformations"]

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#e3f2fd,stroke:#2196f3,color:#000
    style G fill:#fff3e0,stroke:#ff9800,color:#000""",
        "Figure: Linear transformations form the building blocks of neural networks, mapping input vectors through learned weight matrices and bias vectors."
    ),

    "chapter02_calculus_optimization": (
        "Gradient Descent Optimization Loop",
        """graph TD
    A["Initialize Parameters θ₀"] --> B["Forward Pass<br/>Compute Loss L(θ)"]
    B --> C["Backward Pass<br/>Compute ∇L(θ)"]
    C --> D{"Convergence<br/>Check"}
    D -->|No| E["Update Parameters<br/>θ ← θ - η·∇L(θ)"]
    E --> B
    D -->|Yes| F["Optimized<br/>Parameters θ*"]

    G["Learning Rate η"] --> E
    H["Momentum / Adam<br/>Adaptive Updates"] -.-> E

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style F fill:#e3f2fd,stroke:#2196f3,color:#000
    style D fill:#fff3e0,stroke:#ff9800,color:#000""",
        "Figure: The gradient descent optimization loop iteratively updates model parameters by computing gradients and moving in the direction of steepest descent."
    ),

    "chapter03_probability_information": (
        "Information-Theoretic Framework for Deep Learning",
        """graph TD
    A["Data Distribution<br/>P(X)"] --> B["Encoder<br/>P(Z|X)"]
    B --> C["Latent Space<br/>Z"]
    C --> D["Decoder<br/>P(X̂|Z)"]
    D --> E["Reconstruction<br/>X̂"]

    A --> F["Entropy<br/>H(X) = -Σ p log p"]
    B --> G["KL Divergence<br/>D_KL(P‖Q)"]
    G --> H["Cross-Entropy Loss<br/>H(P,Q) = H(P) + D_KL(P‖Q)"]

    F --> H
    H --> I["Training Objective:<br/>Minimize Cross-Entropy"]

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style I fill:#e3f2fd,stroke:#2196f3,color:#000""",
        "Figure: Information theory provides the mathematical foundation for loss functions and representation learning in deep learning."
    ),

    "chapter04_feedforward_networks": (
        "Feed-Forward Neural Network (MLP) Architecture",
        """graph LR
    subgraph Input
        I1["x₁"]
        I2["x₂"]
        I3["x₃"]
        I4["xₙ"]
    end

    subgraph Hidden1["Hidden Layer 1"]
        H1["σ(W₁x + b₁)"]
    end

    subgraph Hidden2["Hidden Layer 2"]
        H2["σ(W₂h₁ + b₂)"]
    end

    subgraph Output
        O1["ŷ = softmax(W₃h₂ + b₃)"]
    end

    I1 --> H1
    I2 --> H1
    I3 --> H1
    I4 --> H1
    H1 -->|"ReLU / Sigmoid<br/>Activation"| H2
    H2 --> O1
    O1 --> L["Loss: L(ŷ, y)"]
    L -->|"Backpropagation"| H1

    style I1 fill:#e8f5e9,stroke:#4caf50,color:#000
    style I2 fill:#e8f5e9,stroke:#4caf50,color:#000
    style I3 fill:#e8f5e9,stroke:#4caf50,color:#000
    style I4 fill:#e8f5e9,stroke:#4caf50,color:#000
    style O1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style L fill:#fff3e0,stroke:#ff9800,color:#000""",
        "Figure: A multi-layer perceptron (MLP) transforms inputs through successive layers of linear transformations and nonlinear activations."
    ),

    "chapter05_convolutional_networks": (
        "Convolutional Neural Network (CNN) Architecture",
        """graph LR
    A["Input Image<br/>H×W×C"] --> B["Conv Layer<br/>Filters + ReLU"]
    B --> C["Pooling<br/>Max/Avg Pool"]
    C --> D["Conv Layer<br/>More Filters + ReLU"]
    D --> E["Pooling<br/>Max/Avg Pool"]
    E --> F["Flatten"]
    F --> G["FC Layer<br/>+ ReLU"]
    G --> H["FC Layer<br/>+ Softmax"]
    H --> I["Class<br/>Predictions"]

    J["Feature Maps:<br/>Local patterns →<br/>Global features"] -.-> B
    J -.-> D

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style B fill:#e3f2fd,stroke:#2196f3,color:#000
    style D fill:#e3f2fd,stroke:#2196f3,color:#000
    style I fill:#fff3e0,stroke:#ff9800,color:#000""",
        "Figure: CNNs build hierarchical feature representations through alternating convolution and pooling layers, from local edges to global object patterns."
    ),

    "chapter06_recurrent_networks": (
        "Recurrent Neural Network Architectures",
        """graph TD
    subgraph RNN["Simple RNN Cell"]
        R1["hₜ = tanh(Wₕhₜ₋₁ + Wₓxₜ + b)"]
    end

    subgraph LSTM["LSTM Cell"]
        direction LR
        F["Forget Gate<br/>fₜ = σ(Wf·[hₜ₋₁,xₜ])"]
        IG["Input Gate<br/>iₜ = σ(Wi·[hₜ₋₁,xₜ])"]
        OG["Output Gate<br/>oₜ = σ(Wo·[hₜ₋₁,xₜ])"]
        C1["Cell State<br/>cₜ = fₜ⊙cₜ₋₁ + iₜ⊙c̃ₜ"]
        HO["Hidden State<br/>hₜ = oₜ⊙tanh(cₜ)"]
        F --> C1
        IG --> C1
        C1 --> HO
        OG --> HO
    end

    subgraph Unrolled["Unrolled Through Time"]
        direction LR
        T1["x₁ → h₁"] --> T2["x₂ → h₂"]
        T2 --> T3["x₃ → h₃"]
        T3 --> T4["... → hₜ"]
    end

    RNN --> LSTM
    LSTM --> Unrolled

    style R1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style C1 fill:#e8f5e9,stroke:#4caf50,color:#000
    style HO fill:#fff3e0,stroke:#ff9800,color:#000""",
        "Figure: RNN architectures process sequential data by maintaining hidden states; LSTM cells add gating mechanisms to control information flow and mitigate vanishing gradients."
    ),

    "chapter07_attention_fundamentals": (
        "Attention Mechanism: Query-Key-Value Framework",
        """graph TD
    Q["Query (Q)<br/>What am I looking for?"] --> S["Score Function<br/>score(Q, Kᵢ)"]
    K["Keys (K)<br/>What do I contain?"] --> S
    S --> SM["Softmax<br/>αᵢ = softmax(scores)"]
    SM --> WS["Weighted Sum<br/>Σ αᵢ · Vᵢ"]
    V["Values (V)<br/>What do I provide?"] --> WS
    WS --> O["Attention Output<br/>Context Vector"]

    subgraph Scoring["Score Functions"]
        S1["Dot Product<br/>QᵀK"]
        S2["Scaled Dot Product<br/>QᵀK / √dₖ"]
        S3["Additive<br/>vᵀtanh(W₁Q + W₂K)"]
    end

    S -.-> Scoring

    style Q fill:#e3f2fd,stroke:#2196f3,color:#000
    style K fill:#e8f5e9,stroke:#4caf50,color:#000
    style V fill:#fff3e0,stroke:#ff9800,color:#000
    style O fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: The attention mechanism computes a weighted combination of values based on the compatibility between queries and keys."
    ),

    "chapter08_self_attention": (
        "Multi-Head Self-Attention Architecture",
        """graph TD
    X["Input Sequence<br/>X ∈ ℝⁿˣᵈ"] --> WQ["W_Q Projection"]
    X --> WK["W_K Projection"]
    X --> WV["W_V Projection"]

    WQ --> Q["Q = X·W_Q"]
    WK --> K["K = X·W_K"]
    WV --> V["V = X·W_V"]

    subgraph MH["Multi-Head Attention (h heads)"]
        direction LR
        H1["Head 1<br/>Attn(Q₁,K₁,V₁)"]
        H2["Head 2<br/>Attn(Q₂,K₂,V₂)"]
        H3["..."]
        Hh["Head h<br/>Attn(Qₕ,Kₕ,Vₕ)"]
    end

    Q --> MH
    K --> MH
    V --> MH

    MH --> CONCAT["Concatenate<br/>All Heads"]
    CONCAT --> WO["Output Projection<br/>W_O"]
    WO --> OUT["Multi-Head<br/>Output ∈ ℝⁿˣᵈ"]

    style X fill:#e8f5e9,stroke:#4caf50,color:#000
    style H1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style H2 fill:#e3f2fd,stroke:#2196f3,color:#000
    style Hh fill:#e3f2fd,stroke:#2196f3,color:#000
    style OUT fill:#fff3e0,stroke:#ff9800,color:#000""",
        "Figure: Multi-head self-attention projects inputs into multiple subspaces, applies parallel attention computations, and concatenates the results."
    ),

    "chapter09_attention_variants": (
        "Attention Mechanism Variants",
        """graph TD
    A["Standard<br/>Full Attention<br/>O(n²)"] --> B["Sparse Attention<br/>Fixed patterns<br/>O(n√n)"]
    A --> C["Linear Attention<br/>Kernel trick<br/>O(n)"]
    A --> D["Local/Sliding<br/>Window Attention<br/>O(n·w)"]
    A --> E["Cross Attention<br/>Encoder-Decoder<br/>O(n·m)"]

    B --> F["Longformer<br/>Local + Global"]
    C --> G["Performer<br/>FAVOR+"]
    D --> H["Sliding Window<br/>+ Dilated"]
    E --> I["Seq2Seq<br/>Translation"]

    style A fill:#f3e5f5,stroke:#9c27b0,color:#000
    style B fill:#e3f2fd,stroke:#2196f3,color:#000
    style C fill:#e8f5e9,stroke:#4caf50,color:#000
    style D fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#fce4ec,stroke:#e91e63,color:#000""",
        "Figure: Various attention variants trade off between computational complexity and expressiveness, each suited to different use cases."
    ),

    "chapter10_transformer_model": (
        "Complete Transformer Encoder-Decoder Architecture",
        """graph TD
    subgraph Encoder["Encoder (N× layers)"]
        direction TB
        EI["Input Embeddings<br/>+ Positional Encoding"] --> ESA["Multi-Head<br/>Self-Attention"]
        ESA --> EAN["Add & LayerNorm"]
        EAN --> EFF["Feed-Forward<br/>Network (FFN)"]
        EFF --> EAN2["Add & LayerNorm"]
    end

    subgraph Decoder["Decoder (N× layers)"]
        direction TB
        DI["Output Embeddings<br/>+ Positional Encoding"] --> DSA["Masked Multi-Head<br/>Self-Attention"]
        DSA --> DAN1["Add & LayerNorm"]
        DAN1 --> DCA["Multi-Head<br/>Cross-Attention"]
        DCA --> DAN2["Add & LayerNorm"]
        DAN2 --> DFF["Feed-Forward<br/>Network (FFN)"]
        DFF --> DAN3["Add & LayerNorm"]
    end

    EAN2 --> DCA

    DAN3 --> LIN["Linear Layer"]
    LIN --> SM["Softmax"]
    SM --> OUT["Output<br/>Probabilities"]

    style EI fill:#e8f5e9,stroke:#4caf50,color:#000
    style DI fill:#e3f2fd,stroke:#2196f3,color:#000
    style ESA fill:#fff3e0,stroke:#ff9800,color:#000
    style DSA fill:#fff3e0,stroke:#ff9800,color:#000
    style DCA fill:#f3e5f5,stroke:#9c27b0,color:#000
    style OUT fill:#fce4ec,stroke:#e91e63,color:#000""",
        "Figure: The Transformer uses stacked encoder and decoder layers with self-attention, cross-attention, and feed-forward networks connected by residual connections and layer normalization."
    ),

    "chapter11_training_transformers": (
        "Transformer Training Pipeline",
        """graph TD
    A["Raw Text Data"] --> B["Tokenization<br/>BPE / WordPiece"]
    B --> C["Batching &<br/>Padding/Masking"]
    C --> D["Forward Pass<br/>Through Transformer"]
    D --> E["Compute Loss<br/>Cross-Entropy"]
    E --> F["Backward Pass<br/>Gradient Computation"]
    F --> G["Optimizer Step<br/>AdamW"]

    G --> H{"Learning Rate<br/>Schedule"}
    H --> I["Warmup Phase<br/>Linear Increase"]
    H --> J["Decay Phase<br/>Cosine / Linear"]

    G --> K["Gradient Clipping<br/>‖g‖ ≤ max_norm"]
    G --> L["Mixed Precision<br/>FP16 / BF16"]

    J --> M["Trained<br/>Model"]

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style D fill:#e3f2fd,stroke:#2196f3,color:#000
    style G fill:#fff3e0,stroke:#ff9800,color:#000
    style M fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Training transformers involves tokenization, batched forward/backward passes, and careful learning rate scheduling with warmup."
    ),

    "chapter12_computational_analysis": (
        "Transformer Computational Complexity Breakdown",
        """graph TD
    A["Input Sequence<br/>Length n, Dim d"] --> B["Self-Attention<br/>O(n²·d)"]
    A --> C["FFN Layer<br/>O(n·d²)"]
    A --> D["Layer Norm<br/>O(n·d)"]
    A --> E["Embedding<br/>O(V·d)"]

    B --> F["Memory: O(n²)<br/>Attention Matrix"]
    C --> G["Memory: O(d²)<br/>FFN Weights"]

    subgraph Bottleneck["Computational Bottleneck"]
        H["n < d: FFN dominates"]
        I["n > d: Attention dominates"]
    end

    B --> Bottleneck
    C --> Bottleneck

    Bottleneck --> J["Total per Layer:<br/>O(n²·d + n·d²)"]
    J --> K["L layers:<br/>O(L·(n²·d + n·d²))"]

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style B fill:#fff3e0,stroke:#ff9800,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style K fill:#e3f2fd,stroke:#2196f3,color:#000""",
        "Figure: Transformer computational cost is dominated by self-attention (quadratic in sequence length) and FFN layers (quadratic in model dimension)."
    ),

    "chapter13_bert": (
        "BERT Architecture and Pre-training",
        """graph TD
    subgraph Pretrain["Pre-training Tasks"]
        direction LR
        MLM["Masked Language<br/>Modeling (MLM)<br/>Predict [MASK] tokens"]
        NSP["Next Sentence<br/>Prediction (NSP)<br/>Classify [CLS]"]
    end

    subgraph Architecture["BERT Encoder Stack"]
        direction TB
        IN["[CLS] tok₁ tok₂ [MASK] tok₄ [SEP] tok₅ tok₆ [SEP]"]
        EMB["Token + Segment +<br/>Position Embeddings"]
        ENC["Transformer Encoder<br/>× 12/24 Layers<br/>Self-Attention + FFN"]
        OUT["Contextual<br/>Representations"]
        IN --> EMB --> ENC --> OUT
    end

    subgraph Finetune["Fine-tuning Tasks"]
        direction LR
        CLS["Classification<br/>[CLS] → Label"]
        NER["Token Tagging<br/>Each token → Tag"]
        QA["Question Answering<br/>Start/End spans"]
    end

    Pretrain --> Architecture
    Architecture --> Finetune

    style MLM fill:#e3f2fd,stroke:#2196f3,color:#000
    style NSP fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#fff3e0,stroke:#ff9800,color:#000
    style CLS fill:#e8f5e9,stroke:#4caf50,color:#000
    style NER fill:#e8f5e9,stroke:#4caf50,color:#000
    style QA fill:#e8f5e9,stroke:#4caf50,color:#000""",
        "Figure: BERT uses a bidirectional Transformer encoder pre-trained with masked language modeling and next sentence prediction, then fine-tuned for downstream tasks."
    ),

    "chapter14_gpt": (
        "GPT Architecture and Autoregressive Generation",
        """graph TD
    subgraph Architecture["GPT Decoder Stack"]
        direction TB
        IN["Input Tokens<br/>tok₁ tok₂ ... tokₜ"]
        EMB["Token + Position<br/>Embeddings"]
        DEC["Transformer Decoder<br/>× 12-96 Layers<br/>Masked Self-Attention + FFN"]
        LM["Language Model Head<br/>Linear + Softmax"]
        OUT["P(tokₜ₊₁ | tok₁...tokₜ)"]
        IN --> EMB --> DEC --> LM --> OUT
    end

    subgraph Training["Training Objective"]
        AR["Autoregressive LM<br/>Maximize P(xₜ|x&lt;t)"]
        CAUSAL["Causal Mask<br/>▼ Triangular"]
    end

    subgraph Scale["GPT Scaling"]
        direction LR
        G1["GPT-1<br/>117M params"]
        G2["GPT-2<br/>1.5B params"]
        G3["GPT-3<br/>175B params"]
        G4["GPT-4<br/>MoE / Multimodal"]
    end

    Training --> Architecture
    Architecture --> Scale

    style DEC fill:#fff3e0,stroke:#ff9800,color:#000
    style AR fill:#e3f2fd,stroke:#2196f3,color:#000
    style G1 fill:#e8f5e9,stroke:#4caf50,color:#000
    style G2 fill:#e8f5e9,stroke:#4caf50,color:#000
    style G3 fill:#e8f5e9,stroke:#4caf50,color:#000
    style G4 fill:#e8f5e9,stroke:#4caf50,color:#000""",
        "Figure: GPT uses a unidirectional Transformer decoder with causal masking, trained autoregressively to predict the next token, scaling from millions to hundreds of billions of parameters."
    ),

    "chapter15_t5_bart": (
        "T5 and BART: Encoder-Decoder Architectures",
        """graph TD
    subgraph T5["T5: Text-to-Text Framework"]
        direction TB
        T5IN["Text Input:<br/>'translate English to French: ...'"]
        T5ENC["Encoder<br/>Bidirectional"]
        T5DEC["Decoder<br/>Autoregressive"]
        T5OUT["Text Output:<br/>'Bonjour le monde'"]
        T5IN --> T5ENC --> T5DEC --> T5OUT
    end

    subgraph BART["BART: Denoising Autoencoder"]
        direction TB
        BIN["Corrupted Input<br/>Masking, Deletion,<br/>Shuffling, Infilling"]
        BENC["Encoder<br/>Bidirectional"]
        BDEC["Decoder<br/>Autoregressive"]
        BOUT["Reconstructed<br/>Original Text"]
        BIN --> BENC --> BDEC --> BOUT
    end

    subgraph Tasks["Unified Tasks"]
        direction LR
        TR["Translation"]
        SUM["Summarization"]
        QAT["Question<br/>Answering"]
        CLT["Classification"]
    end

    T5 --> Tasks
    BART --> Tasks

    style T5ENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style T5DEC fill:#fff3e0,stroke:#ff9800,color:#000
    style BENC fill:#e3f2fd,stroke:#2196f3,color:#000
    style BDEC fill:#fff3e0,stroke:#ff9800,color:#000
    style Tasks fill:#e8f5e9,stroke:#4caf50,color:#000""",
        "Figure: T5 frames all NLP tasks as text-to-text, while BART uses denoising pre-training; both employ the full encoder-decoder Transformer architecture."
    ),

    "chapter16_efficient_transformers": (
        "Efficient Transformer Approaches",
        """graph TD
    A["Standard Attention<br/>O(n²) memory & compute"] --> B["Sparse Patterns"]
    A --> C["Low-Rank<br/>Approximation"]
    A --> D["Kernel Methods"]
    A --> E["Memory<br/>Compression"]

    B --> B1["Longformer<br/>Local + Global Attention"]
    B --> B2["BigBird<br/>Random + Window + Global"]

    C --> C1["Linformer<br/>Project K,V to lower dim"]

    D --> D1["Performer<br/>FAVOR+ Random Features"]

    E --> E1["Compressive<br/>Transformer"]

    subgraph Complexity["Complexity Comparison"]
        direction LR
        O1["Full: O(n²)"]
        O2["Sparse: O(n√n)"]
        O3["Linear: O(n)"]
    end

    B1 --> Complexity
    C1 --> Complexity
    D1 --> Complexity

    style A fill:#fce4ec,stroke:#e91e63,color:#000
    style B1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style C1 fill:#e8f5e9,stroke:#4caf50,color:#000
    style D1 fill:#fff3e0,stroke:#ff9800,color:#000
    style O3 fill:#e8f5e9,stroke:#4caf50,color:#000""",
        "Figure: Efficient Transformer variants reduce the quadratic complexity of standard attention through sparse patterns, low-rank projections, and kernel approximations."
    ),

    "chapter17_vision_transformers": (
        "Vision Transformer (ViT) Architecture",
        """graph TD
    A["Input Image<br/>H × W × C"] --> B["Split into Patches<br/>P × P patches"]
    B --> C["Flatten Patches<br/>N patches × (P²·C)"]
    C --> D["Linear Projection<br/>Patch Embeddings"]
    D --> E["Prepend [CLS] Token<br/>+ Position Embeddings"]

    E --> F["Transformer Encoder<br/>× L Layers"]

    subgraph EncoderBlock["Each Encoder Layer"]
        direction TB
        SA["Multi-Head<br/>Self-Attention"]
        LN1["Layer Norm"]
        FF["MLP / FFN"]
        LN2["Layer Norm"]
        SA --> LN1 --> FF --> LN2
    end

    F --> G["[CLS] Token<br/>Output"]
    G --> H["Classification<br/>Head (MLP)"]
    H --> I["Class<br/>Prediction"]

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style B fill:#e3f2fd,stroke:#2196f3,color:#000
    style F fill:#fff3e0,stroke:#ff9800,color:#000
    style I fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Vision Transformers split images into fixed-size patches, embed them as tokens, and process them through standard Transformer encoder layers."
    ),

    "chapter18_multimodal_transformers": (
        "Multimodal Transformer Architecture",
        """graph TD
    subgraph Inputs["Multi-Modal Inputs"]
        direction LR
        TXT["Text<br/>Tokenizer"]
        IMG["Image<br/>Patch/CNN Encoder"]
        AUD["Audio<br/>Spectrogram"]
    end

    TXT --> TE["Text<br/>Embeddings"]
    IMG --> IE["Visual<br/>Embeddings"]
    AUD --> AE["Audio<br/>Embeddings"]

    TE --> FUSE["Fusion Layer"]
    IE --> FUSE
    AE --> FUSE

    subgraph Fusion["Fusion Strategies"]
        direction LR
        EARLY["Early Fusion<br/>Concatenate &<br/>Joint Attention"]
        CROSS["Cross-Modal<br/>Attention"]
        LATE["Late Fusion<br/>Separate Encoders<br/>→ Merge"]
    end

    FUSE --> TRANS["Shared Transformer<br/>Encoder Layers"]
    TRANS --> OUT["Multi-Modal<br/>Output"]

    Fusion -.-> FUSE

    style TXT fill:#e3f2fd,stroke:#2196f3,color:#000
    style IMG fill:#e8f5e9,stroke:#4caf50,color:#000
    style AUD fill:#fff3e0,stroke:#ff9800,color:#000
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Multimodal Transformers combine text, vision, and audio inputs through various fusion strategies before joint processing in shared Transformer layers."
    ),

    "chapter19_long_context": (
        "Long Context Handling Strategies",
        """graph TD
    A["Long Sequence<br/>n >> typical limit"] --> B["Sliding Window<br/>Local Attention"]
    A --> C["Hierarchical<br/>Chunking"]
    A --> D["Memory<br/>Augmentation"]
    A --> E["Position Encoding<br/>Extensions"]

    B --> B1["Attend to window<br/>of w neighbors"]
    C --> C1["Chunk → Encode<br/>→ Cross-chunk Attn"]
    D --> D1["External Memory<br/>Read/Write"]
    E --> E1["RoPE / ALiBi<br/>Length Extrapolation"]

    subgraph Methods["Notable Methods"]
        direction LR
        M1["Longformer"]
        M2["Memorizing<br/>Transformer"]
        M3["Ring Attention"]
        M4["RoPE Scaling"]
    end

    B1 --> Methods
    D1 --> Methods
    E1 --> Methods

    style A fill:#fce4ec,stroke:#e91e63,color:#000
    style B fill:#e3f2fd,stroke:#2196f3,color:#000
    style C fill:#e8f5e9,stroke:#4caf50,color:#000
    style D fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Long context handling requires specialized techniques to overcome the quadratic attention bottleneck, including windowed attention, hierarchical processing, and position encoding extensions."
    ),

    "chapter20_pretraining_strategies": (
        "Pre-training Strategy Taxonomy",
        """graph TD
    A["Pre-training<br/>Strategies"] --> B["Autoregressive<br/>Language Model"]
    A --> C["Masked Language<br/>Model"]
    A --> D["Denoising<br/>Autoencoder"]
    A --> E["Contrastive<br/>Learning"]

    B --> B1["GPT Family<br/>Predict next token"]
    C --> C1["BERT Family<br/>Predict [MASK] tokens"]
    D --> D1["BART / T5<br/>Reconstruct corrupted text"]
    E --> E1["CLIP / SimCLR<br/>Align representations"]

    subgraph Pipeline["Pre-training Pipeline"]
        direction LR
        P1["Large Corpus<br/>(TB of text)"] --> P2["Tokenize &<br/>Batch"]
        P2 --> P3["Pre-train<br/>(days/weeks)"]
        P3 --> P4["Fine-tune<br/>(hours)"]
        P4 --> P5["Deploy"]
    end

    B1 --> Pipeline
    C1 --> Pipeline
    D1 --> Pipeline

    style A fill:#f3e5f5,stroke:#9c27b0,color:#000
    style B fill:#e3f2fd,stroke:#2196f3,color:#000
    style C fill:#e8f5e9,stroke:#4caf50,color:#000
    style D fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#fce4ec,stroke:#e91e63,color:#000""",
        "Figure: Pre-training strategies define how models learn general representations from large unlabeled corpora before fine-tuning on specific tasks."
    ),

    "chapter21_pytorch_implementation": (
        "PyTorch Transformer Implementation Structure",
        """graph TD
    subgraph Modules["Core nn.Module Classes"]
        direction TB
        EMB["TokenEmbedding<br/>+ PositionalEncoding"]
        MHA["MultiHeadAttention<br/>Q, K, V projections"]
        FFN["FeedForward<br/>Linear → ReLU → Linear"]
        LN["LayerNorm"]
        EL["EncoderLayer<br/>MHA + FFN + LN"]
        DL["DecoderLayer<br/>Masked MHA + Cross MHA + FFN"]
        ENC["TransformerEncoder<br/>N × EncoderLayer"]
        DEC["TransformerDecoder<br/>N × DecoderLayer"]
        FULL["Transformer<br/>Encoder + Decoder + LM Head"]
    end

    EMB --> EL
    MHA --> EL
    FFN --> EL
    LN --> EL
    EL --> ENC
    MHA --> DL
    FFN --> DL
    LN --> DL
    DL --> DEC
    ENC --> FULL
    DEC --> FULL

    FULL --> TR["Training Loop<br/>loss.backward()<br/>optimizer.step()"]

    style FULL fill:#e3f2fd,stroke:#2196f3,color:#000
    style ENC fill:#e8f5e9,stroke:#4caf50,color:#000
    style DEC fill:#fff3e0,stroke:#ff9800,color:#000
    style TR fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: A modular PyTorch implementation of the Transformer, composing small nn.Module building blocks into the full encoder-decoder architecture."
    ),

    "chapter22_hardware_optimization": (
        "Hardware-Aware Optimization Techniques",
        """graph TD
    A["Model Training"] --> B["Memory<br/>Optimization"]
    A --> C["Compute<br/>Optimization"]
    A --> D["Distributed<br/>Training"]

    B --> B1["Gradient<br/>Checkpointing"]
    B --> B2["Mixed Precision<br/>FP16/BF16"]
    B --> B3["Activation<br/>Recomputation"]

    C --> C1["FlashAttention<br/>IO-Aware"]
    C --> C2["Kernel Fusion<br/>Fused Ops"]
    C --> C3["Quantization<br/>INT8/INT4"]

    D --> D1["Data Parallel<br/>(DDP)"]
    D --> D2["Model Parallel<br/>(Tensor/Pipeline)"]
    D --> D3["ZeRO / FSDP<br/>Sharded States"]

    subgraph GPU["GPU Architecture"]
        HBM["HBM (High Bandwidth Memory)"]
        SRAM["SRAM (On-chip)"]
        SM["Streaming Multiprocessors"]
    end

    C1 --> GPU

    style A fill:#f3e5f5,stroke:#9c27b0,color:#000
    style B fill:#e3f2fd,stroke:#2196f3,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style D fill:#e8f5e9,stroke:#4caf50,color:#000
    style C1 fill:#fce4ec,stroke:#e91e63,color:#000""",
        "Figure: Hardware-aware optimization spans memory management, compute efficiency, and distributed training strategies to enable training of large Transformer models."
    ),

    "chapter23_best_practices": (
        "Deep Learning Development Best Practices",
        """graph TD
    A["Problem<br/>Definition"] --> B["Data<br/>Preparation"]
    B --> C["Baseline<br/>Model"]
    C --> D["Iterative<br/>Improvement"]
    D --> E["Evaluation<br/>& Testing"]
    E --> F["Deployment"]
    F --> G["Monitoring<br/>& Maintenance"]

    D --> D1["Hyperparameter<br/>Tuning"]
    D --> D2["Architecture<br/>Search"]
    D --> D3["Regularization<br/>Tuning"]

    B --> B1["Data Cleaning"]
    B --> B2["Augmentation"]
    B --> B3["Train/Val/Test<br/>Splits"]

    E --> E1["Cross-Validation"]
    E --> E2["Ablation Studies"]
    E --> E3["Error Analysis"]

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style D fill:#fff3e0,stroke:#ff9800,color:#000
    style F fill:#e3f2fd,stroke:#2196f3,color:#000
    style G fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: A systematic deep learning development workflow from problem definition through deployment and monitoring."
    ),

    "chapter24_domain_specific_models": (
        "Domain-Specific Model Adaptation Pipeline",
        """graph TD
    A["General Pre-trained<br/>Model (e.g., BERT)"] --> B["Domain-Adaptive<br/>Pre-training (DAPT)"]
    B --> C["Task-Adaptive<br/>Pre-training (TAPT)"]
    C --> D["Fine-tuning on<br/>Domain Task"]
    D --> E["Domain-Specific<br/>Model"]

    F["Domain Corpus<br/>(e.g., Biomedical,<br/>Legal, Scientific)"] --> B

    subgraph Examples["Domain Models"]
        direction LR
        E1["BioBERT<br/>Biomedical"]
        E2["SciBERT<br/>Scientific"]
        E3["LegalBERT<br/>Legal"]
        E4["FinBERT<br/>Financial"]
    end

    E --> Examples

    G["Domain Vocabulary<br/>Custom Tokenizer"] -.-> B

    style A fill:#e3f2fd,stroke:#2196f3,color:#000
    style B fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#e8f5e9,stroke:#4caf50,color:#000
    style F fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Domain-specific models are created by progressively adapting a general pre-trained model through domain and task-specific continued pre-training and fine-tuning."
    ),

    "chapter25_enterprise_nlp": (
        "Enterprise NLP System Architecture",
        """graph TD
    A["Documents<br/>& Text Data"] --> B["Ingestion<br/>Pipeline"]
    B --> C["Pre-processing<br/>Tokenization, Cleaning"]
    C --> D["NLP Models"]

    subgraph Models["NLP Model Stack"]
        direction LR
        M1["Classification"]
        M2["Named Entity<br/>Recognition"]
        M3["Summarization"]
        M4["Search /<br/>Retrieval"]
    end

    D --> Models

    Models --> E["Post-processing<br/>& Aggregation"]
    E --> F["API / Service<br/>Layer"]
    F --> G["Business<br/>Applications"]

    H["Model Registry<br/>& Versioning"] --> D
    I["Feedback Loop<br/>Active Learning"] --> D

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style D fill:#fff3e0,stroke:#ff9800,color:#000
    style F fill:#e3f2fd,stroke:#2196f3,color:#000
    style G fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Enterprise NLP systems combine multiple models in a pipeline architecture with monitoring, versioning, and feedback loops."
    ),

    "chapter26_code_language": (
        "Code Language Model Architecture",
        """graph TD
    A["Source Code<br/>Repository"] --> B["Code Tokenizer<br/>BPE on code"]
    B --> C["Code LM<br/>Transformer Decoder"]

    subgraph Tasks["Code Tasks"]
        direction LR
        T1["Code<br/>Completion"]
        T2["Code<br/>Generation"]
        T3["Code<br/>Translation"]
        T4["Bug<br/>Detection"]
    end

    C --> Tasks

    subgraph Architecture["Model Design"]
        direction TB
        AST["AST-Aware<br/>Encoding"]
        FIM["Fill-in-the-Middle<br/>Training"]
        INST["Instruction<br/>Tuning"]
    end

    Architecture --> C

    subgraph Models["Code Models"]
        direction LR
        CM1["Codex"]
        CM2["CodeLlama"]
        CM3["StarCoder"]
        CM4["DeepSeek<br/>Coder"]
    end

    Tasks --> Models

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style T1 fill:#e3f2fd,stroke:#2196f3,color:#000
    style T2 fill:#e3f2fd,stroke:#2196f3,color:#000""",
        "Figure: Code language models use Transformer architectures adapted for source code with specialized tokenization and training objectives like fill-in-the-middle."
    ),

    "chapter27_video_visual": (
        "Video and Visual Understanding Architecture",
        """graph TD
    A["Video Input<br/>T frames × H × W"] --> B["Frame Sampling<br/>/ Patch Extraction"]
    B --> C["Spatial Encoder<br/>ViT per frame"]
    C --> D["Temporal Encoder<br/>Cross-frame Attention"]
    D --> E["Video<br/>Representation"]

    subgraph Approaches["Architecture Approaches"]
        direction LR
        A1["Joint<br/>Space-Time Attn"]
        A2["Divided<br/>Space then Time"]
        A3["Factorized<br/>Encoder"]
    end

    Approaches -.-> D

    E --> F["Downstream Tasks"]

    subgraph Tasks["Tasks"]
        direction LR
        T1["Action<br/>Recognition"]
        T2["Video<br/>Captioning"]
        T3["Video<br/>QA"]
    end

    F --> Tasks

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#e3f2fd,stroke:#2196f3,color:#000
    style D fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Video Transformers process spatial and temporal dimensions through spatial encoders per frame and temporal attention across frames."
    ),

    "chapter28_knowledge_graphs": (
        "Knowledge Graph-Enhanced Transformer",
        """graph TD
    A["Input Text"] --> B["Text Encoder<br/>Transformer"]
    C["Knowledge Graph<br/>Entities & Relations"] --> D["Graph Encoder<br/>GNN / TransE"]

    B --> E["Knowledge Fusion<br/>Layer"]
    D --> E

    subgraph Fusion["Fusion Methods"]
        direction LR
        F1["Entity<br/>Embedding<br/>Injection"]
        F2["Graph-Guided<br/>Attention"]
        F3["Triple<br/>Integration"]
    end

    Fusion -.-> E

    E --> F["Knowledge-Enhanced<br/>Representations"]
    F --> G["Downstream Tasks"]

    subgraph Tasks["Tasks"]
        direction LR
        T1["Entity<br/>Linking"]
        T2["Relation<br/>Extraction"]
        T3["QA with<br/>Reasoning"]
    end

    G --> Tasks

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#e3f2fd,stroke:#2196f3,color:#000
    style E fill:#fff3e0,stroke:#ff9800,color:#000
    style F fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Knowledge graph-enhanced Transformers fuse structured knowledge with text representations to enable better reasoning and factual grounding."
    ),

    "chapter29_recommendations": (
        "Transformer-Based Recommendation System",
        """graph TD
    A["User Interaction<br/>History"] --> B["Item Sequence<br/>Encoding"]
    B --> C["Transformer<br/>Encoder"]

    D["Item Features<br/>Embeddings"] --> C
    E["User Profile<br/>Embedding"] --> C

    C --> F["Candidate<br/>Scoring"]
    F --> G["Top-K<br/>Recommendations"]

    subgraph Models["Recommendation Models"]
        direction LR
        M1["SASRec<br/>Self-Attention<br/>Sequential"]
        M2["BERT4Rec<br/>Bidirectional<br/>Sequential"]
        M3["PinnerSage<br/>Graph +<br/>Transformer"]
    end

    C --> Models

    H["Side Information<br/>Category, Price,<br/>Time"] -.-> C

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style G fill:#e3f2fd,stroke:#2196f3,color:#000
    style F fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Transformer-based recommendation systems encode user interaction sequences with self-attention to predict relevant items."
    ),

    "chapter30_healthcare": (
        "Healthcare Transformer Pipeline",
        """graph TD
    subgraph Data["Clinical Data Sources"]
        direction LR
        D1["EHR Notes"]
        D2["Medical Images"]
        D3["Lab Results"]
    end

    Data --> B["Pre-processing<br/>De-identification<br/>Normalization"]
    B --> C["Domain Pre-trained<br/>Model (e.g., BioBERT,<br/>ClinicalBERT, Med-PaLM)"]

    subgraph Tasks["Clinical Tasks"]
        direction LR
        T1["Clinical NER<br/>Diseases, Drugs"]
        T2["Diagnosis<br/>Prediction"]
        T3["Medical QA"]
        T4["Radiology<br/>Report Gen"]
    end

    C --> Tasks

    Tasks --> E["Clinical Decision<br/>Support"]
    E --> F["Regulatory<br/>Compliance<br/>(HIPAA, FDA)"]

    style D1 fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#e3f2fd,stroke:#2196f3,color:#000
    style F fill:#fce4ec,stroke:#e91e63,color:#000""",
        "Figure: Healthcare Transformer pipelines process clinical data through domain-specific models with strict regulatory compliance requirements."
    ),

    "chapter31_finance": (
        "Financial Transformer Applications",
        """graph TD
    subgraph Data["Financial Data"]
        direction LR
        D1["Market Data<br/>Prices, Volume"]
        D2["News &<br/>Filings"]
        D3["Earnings<br/>Calls"]
    end

    Data --> B["Financial NLP<br/>Pre-processing"]
    B --> C["FinBERT /<br/>Financial LLM"]

    subgraph Tasks["Financial Tasks"]
        direction LR
        T1["Sentiment<br/>Analysis"]
        T2["Risk<br/>Assessment"]
        T3["Named Entity<br/>Recognition"]
        T4["Report<br/>Generation"]
    end

    C --> Tasks

    Tasks --> E["Trading & Risk<br/>Systems"]
    E --> F["Compliance<br/>& Audit Trail"]

    style D2 fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#e3f2fd,stroke:#2196f3,color:#000
    style F fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Financial Transformer applications process market data, news, and filings through specialized models for sentiment analysis, risk assessment, and automated reporting."
    ),

    "chapter32_legal": (
        "Legal NLP System Architecture",
        """graph TD
    subgraph Data["Legal Documents"]
        direction LR
        D1["Contracts"]
        D2["Case Law"]
        D3["Regulations"]
    end

    Data --> B["Legal NLP<br/>Pre-processing<br/>Section Parsing"]
    B --> C["Legal Transformer<br/>(LegalBERT,<br/>Longformer)"]

    subgraph Tasks["Legal Tasks"]
        direction LR
        T1["Contract<br/>Analysis"]
        T2["Legal<br/>Research"]
        T3["Compliance<br/>Checking"]
        T4["Document<br/>Summarization"]
    end

    C --> Tasks

    Tasks --> E["Legal<br/>Workflow"]
    E --> F["Human Review<br/>& Oversight"]

    G["Long Document<br/>Handling:<br/>Hierarchical Attn"] -.-> C

    style D1 fill:#e8f5e9,stroke:#4caf50,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#e3f2fd,stroke:#2196f3,color:#000
    style F fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: Legal NLP systems use Transformer models adapted for long documents to automate contract analysis, legal research, and compliance checking with human oversight."
    ),

    "chapter33_observability": (
        "ML Observability and Monitoring Stack",
        """graph TD
    A["ML Model<br/>in Production"] --> B["Metrics<br/>Collection"]

    subgraph Metrics["Observability Pillars"]
        direction LR
        M1["Model Quality<br/>Accuracy, F1,<br/>Latency"]
        M2["Data Quality<br/>Drift Detection,<br/>Schema Checks"]
        M3["System Health<br/>GPU Util, Memory,<br/>Throughput"]
    end

    B --> Metrics

    Metrics --> C["Alerting &<br/>Dashboards"]
    C --> D{"Issue<br/>Detected?"}
    D -->|Yes| E["Root Cause<br/>Analysis"]
    D -->|No| F["Continue<br/>Monitoring"]
    E --> G["Remediation<br/>Retrain / Rollback"]
    G --> A

    subgraph Tools["Observability Tools"]
        direction LR
        T1["Prometheus<br/>+ Grafana"]
        T2["MLflow<br/>Tracking"]
        T3["Evidently<br/>Data Drift"]
    end

    Tools -.-> B

    style A fill:#e3f2fd,stroke:#2196f3,color:#000
    style C fill:#fff3e0,stroke:#ff9800,color:#000
    style E fill:#fce4ec,stroke:#e91e63,color:#000
    style G fill:#e8f5e9,stroke:#4caf50,color:#000""",
        "Figure: ML observability monitors model quality, data quality, and system health to detect issues early and enable rapid remediation."
    ),

    "chapter34_dsl_agents": (
        "LLM Agent System Architecture",
        """graph TD
    A["User Query"] --> B["LLM Agent<br/>(Planning & Reasoning)"]

    B --> C["Tool Selection"]

    subgraph Tools["Available Tools"]
        direction LR
        T1["Code<br/>Executor"]
        T2["Web<br/>Search"]
        T3["Database<br/>Query"]
        T4["API<br/>Calls"]
    end

    C --> Tools
    Tools --> D["Observation<br/>/ Result"]
    D --> B

    B --> E{"Task<br/>Complete?"}
    E -->|No| C
    E -->|Yes| F["Final<br/>Response"]

    subgraph Framework["Agent Framework"]
        direction LR
        F1["ReAct<br/>Reason + Act"]
        F2["Chain-of-Thought<br/>Reasoning"]
        F3["DSL / Function<br/>Calling"]
    end

    Framework -.-> B

    G["Memory /<br/>Context Window"] -.-> B

    style A fill:#e8f5e9,stroke:#4caf50,color:#000
    style B fill:#fff3e0,stroke:#ff9800,color:#000
    style F fill:#e3f2fd,stroke:#2196f3,color:#000
    style D fill:#f3e5f5,stroke:#9c27b0,color:#000""",
        "Figure: LLM agent systems use a reasoning-action loop where the LLM plans, selects tools, observes results, and iterates until the task is complete."
    ),
}


def inject_diagram(filepath, diagram_title, mermaid_code, caption):
    """Inject a Mermaid diagram into a chapter HTML file after Learning Objectives."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if diagram already exists
    if 'architecture-diagram' in content:
        print(f"  SKIP (already has diagram): {filepath}")
        return False

    diagram_html = f"""
<div class="architecture-diagram">
<h3>{diagram_title}</h3>
<pre class="mermaid">
{mermaid_code}
</pre>
<p class="diagram-caption">{caption}</p>
</div>

"""

    # Strategy 1: Insert after </ol> that follows Learning Objectives
    # Look for the pattern: Learning Objectives heading followed by an <ol>...</ol>
    pattern = r'(<h3>Learning Objectives</h3>.*?</ol>)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + "\n" + diagram_html + content[insert_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK (after Learning Objectives): {os.path.basename(filepath)}")
        return True

    # Strategy 2: Insert after the first </p> following "Chapter Overview"
    pattern2 = r'(<h2>Chapter Overview</h2>\s*<p>.*?</p>)'
    match2 = re.search(pattern2, content, re.DOTALL)

    if match2:
        insert_pos = match2.end()
        content = content[:insert_pos] + "\n" + diagram_html + content[insert_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK (after Chapter Overview): {os.path.basename(filepath)}")
        return True

    # Strategy 3: Insert after the first <h1>...</h1> and any following <p>
    pattern3 = r'(<h1>.*?</h1>\s*(?:<p>.*?</p>\s*)*)'
    match3 = re.search(pattern3, content, re.DOTALL)

    if match3:
        insert_pos = match3.end()
        content = content[:insert_pos] + "\n" + diagram_html + content[insert_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK (after h1): {os.path.basename(filepath)}")
        return True

    print(f"  FAIL (no insertion point found): {filepath}")
    return False


def main():
    success = 0
    fail = 0
    skip = 0

    for chapter_id, (title, mermaid_code, caption) in DIAGRAMS.items():
        filepath = os.path.join(CHAPTERS_DIR, f"{chapter_id}.html")
        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {filepath}")
            fail += 1
            continue

        result = inject_diagram(filepath, title, mermaid_code, caption)
        if result:
            success += 1
        elif result is False:
            skip += 1
        else:
            fail += 1

    print(f"\nDone: {success} injected, {skip} skipped, {fail} failed")
    print(f"Total chapters with diagrams defined: {len(DIAGRAMS)}")


if __name__ == "__main__":
    main()
