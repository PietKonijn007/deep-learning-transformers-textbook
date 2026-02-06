# Content Reduction Proposal

**Goal:** Reduce the deep tech book from ~800 pages to ~600 pages by eliminating redundancy, consolidating repeated content, and trimming verbose sections.

**How to use this document:** Each proposal is numbered and independent. Review them one by one and mark APPROVE or REJECT. Proposals are ordered by estimated page savings (highest first). Approved proposals can be implemented incrementally.

**Estimated total savings:** ~220–270 pages (from ~33,900 lines of LaTeX)

---

## Implementation Progress

| Category | Status | Lines Removed | Files Changed |
|----------|--------|--------------|---------------|
| **B: Within-Chapter Verbosity Cuts** | **DONE** | **~1,838** | **15 files** |
| **A1: Consolidate Drift Sections** | **DONE** | **~619** | **8 files** |
| **A2+A3+A4: Exclude Solutions from PDF** | **DONE** | **~10,809** (from PDF) | **35 files** |
| **A6: Ch21/22/23 Triple Coverage** | **DONE** | **~30** | **3 files** |
| **A7: BERT-base Consolidation** | **DONE** | **~105 net** | **9 files** |
| A5: Hardware Analysis Consolidation | Not started | — | — |
| C: Duplicate Section Removals | Not started | — | — |
| D: Minor Cleanups | **DONE** (D1, D2 included in B) | included above | — |

**Total lines before Category B:** 33,904 | **After B:** 32,119 | **After A1:** ~31,500 | **After A2 (PDF):** ~20,691 | **After A6+A7:** ~20,556 | **Net PDF reduction:** ~13,348 lines (~267 pages)

---

## Table of Contents

- [Category A: Structural / Cross-Chapter Consolidations](#category-a-structural--cross-chapter-consolidations) (~120–150 pages)
- [Category B: Within-Chapter Verbosity Cuts](#category-b-within-chapter-verbosity-cuts) (~60–75 pages) **[IMPLEMENTED]**
- [Category C: Duplicate Section Removals](#category-c-duplicate-section-removals) (~30–40 pages)
- [Category D: Minor Cleanups](#category-d-minor-cleanups) (~10–15 pages)
- [Summary Table](#summary-table)

---

## Category A: Structural / Cross-Chapter Consolidations

These are high-impact changes that address content repeated across many chapters.

---

### A1. Consolidate "Continuous Learning and Model Drift" into Chapter 24

**Status:** [x] IMPLEMENTED

**Problem:** Chapters 24–33 (10 chapters) each contain a near-identical "Continuous Learning and Model Drift" section following the same template: drift types → detecting drift → strategies for continuous learning → practical implementation → cross-domain patterns. The template alone accounts for ~1,000–1,200 lines of highly repetitive content.

**Current state (lines dedicated to drift per chapter):**

| Chapter | Drift Section Lines | % of Chapter |
|---------|-------------------|--------------|
| Ch24 Domain-Specific Models | ~78 | 14% |
| Ch25 Enterprise NLP | ~100 | 19% |
| Ch26 Code Language | ~102 | 20% |
| Ch27 Video/Visual | ~100+ | 15% |
| Ch29 Recommendations | ~127 | 22% |
| Ch30 Healthcare | ~135 | 15% |
| Ch31 Finance | ~145 | **33%** |
| Ch32 Legal | ~141 | **30%** |
| Ch33 Observability | ~135 | 23% |
| Ch34 DSL/Agents (synthesis) | ~97 | 16% |

**Proposal:** Keep Chapter 24 as the canonical home for the generic drift framework (drift types, detection strategies, continuous learning strategies, MLOps infrastructure). In each domain chapter (25–33), replace the full drift section with a short (10–15 line) domain-specific addendum that covers ONLY what is unique to that domain (e.g., "alpha decay" in finance, "case law evolution" in legal, "API deprecation" in code). Remove the generic framework, business impact template, and cross-domain patterns subsections from each domain chapter. In Ch34, replace the 97-line synthesis prose with a single comparison table.

**Estimated savings:** ~900–1,000 lines → **~20–25 pages**

**Actual savings:** 619 lines removed across 8 files (Ch25, Ch26, Ch27, Ch29, Ch30, Ch32, Ch33, Ch34). Ch31 was already condensed in B15. Ch24 retained as canonical framework. Each domain chapter now keeps only its unique drift patterns + a keypoint referencing Ch24 + domain-specific strategies as bullet points. Ch34 synthesis replaced with comparison table + 3 universal principles.

---

### A2. Cut Exercise Solutions by 50–60% Across Chapters 10–20

**Status:** [x] IMPLEMENTED (global solution exclusion — see note below)

**Problem:** Across chapters 10–20, exercise solutions consume 7,834 lines — **49% of all content** in those 11 chapters. Some chapters are worse than others:

| Chapter | Total Lines | Solution Lines | Solutions % |
|---------|-----------|---------------|-------------|
| Ch18 Multimodal | 1,836 | 1,297 | **71%** |
| Ch17 Vision Transformers | 1,657 | 1,067 | **64%** |
| Ch16 Efficient Transformers | 1,146 | 635 | **55%** |
| Ch15 T5/BART | 1,593 | 866 | **54%** |
| Ch14 GPT | 1,338 | 710 | **53%** |
| Ch13 BERT | 1,189 | 616 | **52%** |
| Ch19 Long Context | 1,212 | 630 | **52%** |
| Ch11 Training | 2,366 | 976 | **41%** |
| Ch12 Computational | 1,414 | 485 | **34%** |
| Ch10 Transformer Model | 1,276 | 324 | **25%** |
| Ch20 Pretraining | 940 | 228 | **24%** |

Solutions currently include complete runnable Python implementations with benchmarks, training loops, and sample outputs. The proposal is to shorten solutions to show the key algorithmic idea (pseudocode or core 10–20 lines) without full training infrastructure, and move complete implementations to an online companion repository.

**Estimated savings:** ~4,000–4,500 lines → **~80–100 pages**

**Actual implementation:** Rather than shortening solutions, all `\begin{solution}...\end{solution}` blocks are excluded from PDF compilation via `\excludecomment{solution}` (LaTeX `comment` package) in `main_pro.tex`. Solutions remain in the `.tex` source files and are still converted to HTML for the companion website. Each chapter's `\section{Solutions}` now includes a reference directing PDF readers to `https://deeplearning.hofkensvermeulen.be`. This approach was applied globally to all 34 chapters, also accomplishing A3 and A4. Total: 10,809 lines excluded from PDF across 34 chapters. To re-include solutions, comment out `\excludecomment{solution}` in `main_pro.tex`.

---

### A3. Cut Exercise Solutions by 40–50% Across Chapters 1–9

**Status:** [x] IMPLEMENTED (included in A2 global solution exclusion)

**Problem:** Chapters 1–9 also have substantial solution sections:

| Chapter | Solution Lines | Solutions % |
|---------|---------------|-------------|
| Ch2 Calculus/Optimization | 349 | 24% |
| Ch1 Linear Algebra | 306 | 34% |

Exercises 5–8 in Ch1 are increasingly specialized hardware/FLOP calculations that overlap with later chapters. Ch2 has 9 exercises with full solutions, several on distributed training efficiency and gradient checkpointing implementation.

**Proposal:** Remove 2–3 exercises per chapter that overlap with later chapters or are overly specialized hardware calculations. Shorten remaining solutions.

**Estimated savings:** ~300 lines → **~6–8 pages**

---

### A4. Cut Exercise Solutions by 40–50% Across Chapters 21–34

**Status:** [x] IMPLEMENTED (included in A2 global solution exclusion)

**Problem:** Ch28 Knowledge Graphs has 266 lines of solutions (20% of chapter), Ch30 Healthcare has 220 lines (25%), and Ch21 PyTorch Implementation has 200 lines (10%).

**Proposal:** Same approach as A2 — shorten to key ideas, move full implementations to online companion.

**Estimated savings:** ~400 lines → **~8–10 pages**

---

### A5. Consolidate All Hardware Analysis into Chapters 12 and 22

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** Nearly every chapter in Parts I–VI (chapters 1–20) contains extensive GPU/hardware analysis covering: A100 specs (312 TFLOPS, 1.5 TB/s), arithmetic intensity calculations, compute-bound vs memory-bound analysis, batch size impact on GPU utilization, memory bandwidth calculations, and Tensor Core alignment requirements. Estimated total: ~800–1,000 lines scattered across 15+ chapters.

**Specific locations of hardware tangents in non-hardware chapters:**

| Chapter | Section | Lines | Content |
|---------|---------|-------|---------|
| Ch1 | "Hardware Context for Matrix Operations" | 251–308 | Row-major/column-major, BLAS, A100 specs, blocking |
| Ch2 | "Hardware Considerations for Gradient Computation" | 928–1090 | GPU vs CPU gradients, mixed precision, distributed sync |
| Ch3 | "Hardware Implications of Softmax" | 257–306 | GPU bandwidth for softmax, vocabulary optimization |
| Ch4 | "Memory and Computation Analysis" | 140–198 | GPU utilization at different batch sizes, CUDA core % |
| Ch4 | "Computational Cost of Activation Functions" | 226–254 | ReLU vs GELU runtime, fused kernels |
| Ch4 | "Computational Overhead of Dropout" | 363–401 | cuRAND timing, dropout memory |
| Ch5 | "Hardware Optimization for Convolutions" | 238–293 | Tensor Cores, cuDNN, im2col |
| Ch7 | "Hardware Implications of Attention" | 613–693 | Parallelization, memory bandwidth, batch processing |
| Ch8 | "Hardware Considerations and Memory Layout" | 132–141 | Attention matrix memory |
| Ch8 | "Tensor Core Utilization" | 263–271 | Head dimension alignment |
| Ch9 | "Implementation Considerations" | 483–494 | GPU alignment, kernel fusion |

**Proposal:** Reduce each of these to a 2–3 sentence "keypoint" box with a cross-reference to Ch12 (Computational Analysis) or Ch22 (Hardware Optimization) where the full treatment lives. Keep only the topic-specific numbers (e.g., "attention is memory-bound for n > 1024") and remove the generic GPU analysis.

**Estimated savings:** ~500–600 lines → **~10–15 pages**

---

### A6. Eliminate Triple Coverage of Optimization Topics Across Chapters 21, 22, 23

**Status:** [x] IMPLEMENTED

**Problem:** Chapters 21 (PyTorch Implementation), 22 (Hardware Optimization), and 23 (Best Practices) all cover mixed precision training, gradient checkpointing, quantization, distillation, KV caching, inference optimization (ONNX, TensorRT), serving frameworks, and hardware selection with significant overlap. Ch23 is essentially an abbreviated retelling of Ch21 and Ch22.

**Specific duplications:**

| Topic | Ch21 Lines | Ch22 Lines | Ch23 Lines |
|-------|-----------|-----------|-----------|
| Mixed precision | 192–236 | ~100–150 | 118–125 |
| Gradient checkpointing | 283–327 | mentioned | 110–117 |
| Memory profiling | 348–477 | — | 87–133 |
| Quantization | 781–840 | 225–319 | 235–243 |
| ONNX/TensorRT | 663–779 | 485–524 | mentioned |
| Serving/deployment | — | 525–567 | 302–344 |
| Hardware selection | — | 568–626 | 253–259 |

**Proposal:** Make Ch21 the canonical implementation reference (code-focused), Ch22 the canonical hardware/compression reference (theory-focused). Restructure Ch23 as a concise decision-making guide (~300–400 lines) with flowcharts, decision tables, and cross-references instead of restating technical details.

**Estimated savings:** ~400 lines → **~8–10 pages**

**Actual implementation:** B10, B11, and B12 already accomplished the bulk of A6 (removing Ch21's redundant second implementation, Ch22's "in practice" restatements, and restructuring Ch23 as a decision guide). The remaining A6 work converted Ch23's learning rate and batch size sections from prose explanations to decision tables, replaced the gradient analysis code block with a brief reference to Ch21, fixed an ONNX Runtime speedup discrepancy between Ch21 (was "20-40%") and Ch22 (1.5-2×) — now consistent at 1.5-2×, and added cross-references between all three chapters (Ch21↔Ch22 for quantization, ONNX, TensorRT, KV cache). Net: ~30 lines trimmed from Ch23 + quality improvements.

---

### A7. Consolidate BERT-base Parameter/FLOP Calculations into One Canonical Location

**Status:** [x] IMPLEMENTED (canonical location: Ch1 Section 1.X "BERT-base: A Canonical Worked Analysis")

**Problem:** The same BERT-base analysis (110M params, 12 layers, d=768, n=512) was derived from scratch in at least 9 chapters.

**Implementation:** Created a comprehensive canonical section in Chapter 1 (`\label{sec:bert_base_analysis}`) covering architecture specification, parameter count (per-layer + complete model), dimension tracking, activation memory, FLOPs analysis, training memory budget, and hardware timing. Replaced detailed derivations in Ch2, Ch4, Ch7, Ch8, Ch10 (two examples), Ch12, Ch13 with condensed summaries + `Section~\ref{sec:bert_base_analysis}` cross-references. Ch15 (BART-large) retained its unique content with a methodology reference added.

**Lines saved:** ~220 lines removed from Ch2/Ch4/Ch7/Ch8/Ch10/Ch12/Ch13, ~115 lines added to Ch1 canonical section → **~105 net lines removed (~2 pages)**. Primary benefit is eliminating 8× redundancy rather than raw line count.

---

## Category B: Within-Chapter Verbosity Cuts

These target specific sections that are excessively wordy within a single chapter.

---

### B1. Chapter 11: Condense Training Cost Estimation and Practical Recipe

**Status:** [x] IMPLEMENTED

**Problem:** Ch11 (2,366 lines — the longest chapter) has three verbose sections:
- "Training Cost Estimation" (lines 1087–1251, ~165 lines): Extremely detailed GPT-3 cost analysis with hardware costs, energy costs, cloud vs on-premise comparison. This same analysis appears in Ch10, Ch12, Ch14, and Ch20.
- "Practical Training Recipe" (lines 1252–1353, ~100 lines): Largely summarizes advice already given earlier in the same chapter.
- "Distributed Training Strategies" (lines 730–852, ~120 lines): Very verbose prose for data/model/pipeline/tensor parallelism with worked examples that reappear in Ch12, Ch18, Ch20.

**Proposal:** Cut training cost estimation to a single concise table with one worked example (~40 lines). Remove the "Practical Training Recipe" section (it's a recap). Condense distributed training prose by 50%.

**Estimated savings:** ~250 lines → **~5–6 pages**

---

### B2. Chapter 2: Condense Adam Optimizer and Hardware Sections

**Status:** [x] IMPLEMENTED

**Problem:** Ch2 (1,441 lines) devotes ~145 lines to Adam across 4 subsections ("Intuition Behind Adam", "Understanding Each Component", "Why Adam Works Better", "Practical Considerations"). The "Why Adam Works Better" list rehashes what the math already showed. "Practical Considerations" is a hyperparameter list that could be a single table.

Additionally, "Hardware Considerations for Gradient Computation" (lines 928–1090, 162 lines) covers mixed precision, gradient accumulation, and distributed gradient sync — topics better suited to Ch11 or Ch22.

**Proposal:** Condense Adam to ~80 lines (one clear derivation + one keypoint box + one table of hyperparameters). Move hardware considerations to a ~20-line keypoint referencing Ch11/Ch22.

**Estimated savings:** ~180 lines → **~4 pages**

---

### B3. Chapter 3: Remove Hardware Tangent from Probability Chapter

**Status:** [x] IMPLEMENTED

**Problem:** Ch3 (521 lines) pivots from probability theory into GPU engineering midway through. "Cross-Entropy Loss: Computational and Memory Analysis" (lines 165–201) computes logits memory for BERT/GPT-2/GPT-3. "Hardware Implications of Softmax and Large Vocabularies" (lines 257–306) covers GPU bandwidth, vocabulary impact on training speed, and optimization techniques (sampled softmax, adaptive softmax, vocabulary pruning). Almost none of this is probability theory.

**Proposal:** Reduce lines 165–306 to a single 20-line "Practical Considerations" keypoint box. Move detailed hardware analysis to Ch12.

**Estimated savings:** ~120 lines → **~2–3 pages**

---

### B4. Chapter 4: Trim Hardware Analysis from Feed-Forward Networks

**Status:** [x] IMPLEMENTED

**Problem:** Ch4 (539 lines) buries its core MLP/activation/initialization content under hardware analysis:
- "Memory and Computation Analysis" (lines 140–198): GPU utilization at different batch sizes, CUDA core utilization percentages
- "Computational Cost of Activation Functions" (lines 226–254): ReLU vs GELU runtime with FLOPs-per-element and bandwidth analysis. Conclusion (GELU adds ~1–2% training time) could be 2 sentences.
- "Computational Overhead of Dropout" (lines 363–401): cuRAND timing, dropout memory, inference mode differences

**Proposal:** Cut each hardware subsection to a 3–5 line summary with key takeaway. Full analysis belongs in Ch12/Ch22.

**Estimated savings:** ~100 lines → **~2 pages**

---

### B5. Chapter 5: Move ViT Comparison Out of CNN Fundamentals

**Status:** [x] IMPLEMENTED

**Problem:** Ch5 (492 lines) contains a 47-line "Parameter Efficiency: CNNs vs Transformers" section (lines 189–236) comparing CNNs to Vision Transformers, including accuracy numbers, parameter breakdowns, and hybrid architectures (CvT, Swin). This forward-references ViT (Ch17) which hasn't been introduced yet.

Additionally, "Hardware Optimization for Convolutions" (lines 238–293, 55 lines) covers Tensor Cores, cuDNN, and memory bandwidth in a CNN fundamentals chapter.

**Proposal:** Move the ViT comparison to Ch17 where it belongs. Reduce hardware section to a keypoint box.

**Estimated savings:** ~80 lines → **~2 pages**

---

### B6. Chapter 7: Remove Duplicated Attention Scoring Comparison and RNN Rehash

**Status:** [x] IMPLEMENTED

**Problem:** Ch7 (868 lines) has two redundant sections:
- "Attention Score Computation Methods" (lines 444–516): Re-describes all four attention mechanisms (Bahdanau, dot-product, scaled dot-product, general) that were already introduced earlier in the same chapter. The Bahdanau description repeats lines 80–104 nearly verbatim.
- "Hardware Implications of Attention" (lines 613–693, 80 lines): The "Parallelization: RNNs vs Attention" subsection (lines 618–643) is a near-complete repetition of Ch6's "RNNs vs Transformers" section. Contains a self-noted calculation error at line 690.

**Proposal:** Remove the duplicated scoring comparison (lines 444–516) — keep only the comparison table. Cut the RNN rehash from the hardware section and fix or remove the calculation error.

**Estimated savings:** ~120 lines → **~2–3 pages**

---

### B7. Chapter 15: Remove Self-Duplicated T5 Model Sizes

**Status:** [x] IMPLEMENTED

**Problem:** In Ch15, lines 224–232 present five T5 model sizes (Small, Base, Large, 3B, 11B) as verbose prose paragraphs. Then lines 234–261 present the **exact same data** as a bulleted list. The information is literally duplicated within the same section.

**Proposal:** Delete the prose paragraphs (lines 224–232), keeping only the concise list format.

**Estimated savings:** ~40 lines → **~1 page**

---

### B8. Chapter 18: Condense Fusion Strategies and Computational Analysis

**Status:** [x] IMPLEMENTED

**Problem:** Ch18 (1,836 lines) has verbose prose in:
- "Fusion Strategies" (lines 24–101, 80 lines): Early/late/cross-modal fusion each get multi-paragraph treatments for straightforward concepts
- "Computational Analysis of Multimodal Transformers" (lines 300–370, 70 lines): Re-derives FLOPs formulas, memory budgets, and training costs using identical methodology to Ch12
- "Training Challenges" (lines 333–370, 35 lines): Repeats distributed training concepts from Ch11

**Proposal:** Condense fusion strategies to ~40 lines with a comparison table. Cut computational analysis to multimodal-specific deltas referencing Ch12. Remove distributed training restating.

**Estimated savings:** ~100 lines → **~2 pages**

---

### B9. Chapter 10: Remove Premature Computational Analysis and Variant Previews

**Status:** [x] IMPLEMENTED

**Problem:** Ch10 (1,276 lines) contains:
- "Computational Complexity and Hardware Analysis" (lines 495–655, ~160 lines): Duplicates nearly all of Ch12's core material. This reads like a preview of Ch12 within the architecture chapter.
- "Transformer Variants" (lines 829–921): Previews BERT, GPT, and T5/BART architectures that each get their own dedicated chapters (Ch13, Ch14, Ch15).

**Proposal:** Cut computational section to a 20-line overview with forward reference to Ch12. Condense variants to a one-paragraph overview with chapter references.

**Estimated savings:** ~180 lines → **~4 pages**

---

### B10. Chapter 21: Eliminate Redundant Second Implementation Pass

**Status:** [x] IMPLEMENTED

**Problem:** Ch21 (1,975 lines) contains:
- "Complete Implementation Examples" (lines 975–1200, ~225 lines): Re-implements MultiHeadAttention, FeedForward, TransformerLayer, and TransformerModel classes that were already shown in earlier sections of the same chapter, with minor variations (combined QKV projection, FusedLayerNorm).
- "Optimized Training Loop" (lines 1202–1327, ~125 lines): A second full training loop duplicating the earlier training pipeline section.

**Proposal:** Integrate the unique optimizations (combined QKV, FusedLayerNorm) into the original implementation sections. Remove the second training loop.

**Estimated savings:** ~250 lines → **~5–6 pages**

---

### B11. Chapter 22: Remove "In Practice" Restatement Subsections

**Status:** [x] IMPLEMENTED

**Problem:** Ch22 has three "...in Practice" subsections that simply restate the preceding formal treatment in prose:
- "Quantization in Practice" (lines 309–319): Restates lines 225–307
- "Pruning in Practice" (lines 371–379): Restates lines 321–370
- "Distillation in Practice" (lines 410–418): Restates lines 381–409

Each begins with a sentence that is essentially the definition of the technique it follows.

**Proposal:** Delete all three subsections. The formal treatments are clear on their own.

**Estimated savings:** ~30 lines → **~1 page**

---

### B12. Chapter 23: Restructure as Decision Guide, Not Technical Recap

**Status:** [x] IMPLEMENTED

**Problem:** Ch23 (1,056 lines) functions as an abbreviated retelling of Ch21 and Ch22. Nearly every section has a more detailed counterpart:
- "Memory Management" (lines 87–133) → Ch21 memory profiling
- "Inference Optimization" (lines 214–260) → Ch21 + Ch22
- "Production Deployment" (lines 302–344) → Ch22
- "Common Training Issues" (lines 204–212) → Ch21 debugging

**Proposal:** Restructure Ch23 to be a concise decision-making reference with flowcharts, decision tables, and checklists that cross-reference Ch21/Ch22 for details. Preserve unique content (model selection guidance, cost analysis, case studies). Remove duplicate technical explanations.

**Estimated savings:** ~300 lines → **~6–8 pages**

---

### B13. Chapter 6: Trim RNN vs Transformer Comparison

**Status:** [x] IMPLEMENTED

**Problem:** Ch6's "RNNs vs Transformers: A Computational Comparison" (lines 345–401, 56 lines) contains 5 subsections making the same argument from different angles. The training time estimation (lines 370–380) involves speculative calculations about a hypothetical LSTM-based BERT that was never built. This entire comparison is repeated in Ch7 (lines 613–693) at even greater length.

**Proposal:** Reduce to a single comparison table + 10-line narrative in Ch6. Let Ch7 handle the detailed argument from the attention perspective, or vice versa — pick one canonical location.

**Estimated savings:** ~40 lines → **~1 page**

---

### B14. Chapter 28: Tighten Case Study and Cross-Chapter Connections

**Status:** [x] IMPLEMENTED

**Problem:** Ch28 (1,316 lines — second longest in Part VII–X) has:
- Case study data sources (lines 982–995) and schema (lines 996–1003): Verbose descriptions of standard enterprise data patterns
- "Cross-Chapter Connections" (lines 864–900, 37 lines): Shallow observations like "NER and relation extraction (Chapter 25) populate knowledge graphs"
- Duplicate `\subsection{Type Constraints}` headers at lines 264 and 266

**Proposal:** Condense case study to essential architecture decisions. Reduce cross-chapter connections to a bullet list. Fix the duplicate subsection header.

**Estimated savings:** ~60 lines → **~1–2 pages**

---

### B15. Chapter 31: Reduce Drift Section from 33% to ~10% of Chapter

**Status:** [x] IMPLEMENTED

**Problem:** Ch31 Finance (439 lines) devotes 145 lines — **33% of the chapter** — to drift content. This is the worst ratio of any chapter. The finance-specific patterns (regime shifts, alpha decay, adversarial fraud) are valuable, but the generic framework, 6-item business impact list, detection strategies, and MLOps practices are template content.

**Proposal:** (This is a specific instance of A1, but called out because of severity.) Keep only the finance-specific drift patterns (~30 lines). Remove everything that is generic MLOps advice restated with financial vocabulary.

**Estimated savings:** ~115 lines → **~2–3 pages** (included in A1 estimate)

---

## Category C: Duplicate Section Removals

These target specific sections that are near-identical copies of content in another chapter.

---

### C1. Remove Longformer/BigBird Duplication Between Ch16 and Ch19

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** This is the most egregious duplication in the book. The descriptions are near-identical, including the same definitions, complexity formulas, memory calculations, and benchmark numbers:
- Ch16 Efficient Transformers: Longformer (lines 78–143, ~65 lines) + BigBird (lines 145–216, ~70 lines)
- Ch19 Long Context: Longformer (lines 156–183, ~28 lines) + BigBird (lines 185–209, ~25 lines)

**Proposal:** Keep Ch16 as the canonical home for the mechanism descriptions (with TikZ diagrams). In Ch19, replace with a 5-line summary + "see Chapter 16 for details" reference, then focus only on how these mechanisms are applied in long-context scenarios.

**Estimated savings:** ~50 lines → **~1 page**

---

### C2. Remove Efficient Attention Preview from Ch8 (Covered in Ch9/Ch16)

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** Ch8 "Memory-Efficient Attention Variants" (lines 487–526, 39 lines) previews sparse, linear, and low-rank attention that are covered in full detail in Ch9 (lines 359–494, 135 lines) and Ch16 (entire chapter).

**Proposal:** Replace the Ch8 preview with a single paragraph: "Several approaches exist to reduce the quadratic complexity of attention, including sparse, linear, and low-rank variants. These are covered in detail in Chapters 9 and 16."

**Estimated savings:** ~35 lines → **~1 page**

---

### C3. Remove Scoring Function Re-Listing from Ch9

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** Ch9 "Alternative Attention Scoring Functions" (lines 117–147, 30 lines) re-lists all four scoring functions (Bahdanau, Luong, scaled dot-product, general) that were already defined and compared in Ch7 (lines 444–516). The comparison at lines 142–147 is a simplified version of Ch7's table.

**Proposal:** Replace with a 3-line reference to Ch7's comparison table.

**Estimated savings:** ~25 lines → **~0.5 pages**

---

### C4. Consolidate GPT-3 Training Cost Analysis into Ch11

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** The same GPT-3 training cost breakdown appears in 5 chapters:
- Ch10 (within lines 495–655)
- Ch11 (lines 1087–1251, ~165 lines — the most detailed)
- Ch12 (referenced in scaling context)
- Ch14 (lines 250–283, ~35 lines)
- Ch20 (lines 383–420, ~40 lines)

**Proposal:** Keep Ch11 as the canonical location. In Ch10, Ch14, and Ch20, replace with a 1–2 sentence reference to Ch11.

**Estimated savings:** ~100 lines → **~2 pages**

---

### C5. Consolidate Scaling Laws into One Chapter

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** Kaplan et al. and Chinchilla scaling laws are presented in three chapters:
- Ch12 (lines 883–908, ~25 lines)
- Ch14 (lines 406–469, ~65 lines — most detailed)
- Ch20 (lines 283–304, ~20 lines)

**Proposal:** Keep the full treatment in Ch14 (GPT chapter, where scaling laws are most relevant historically). Replace Ch12 and Ch20 occurrences with brief references.

**Estimated savings:** ~45 lines → **~1 page**

---

### C6. Consolidate KV Caching into Ch14

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** KV caching is derived and explained in three chapters:
- Ch10 (within computational section)
- Ch12 (lines 678–767, ~90 lines)
- Ch14 (lines 288–339, ~50 lines)

**Proposal:** Keep the full treatment in Ch14 (the GPT/autoregressive chapter where KV caching is most relevant). Ch12 can have a brief summary with forward reference.

**Estimated savings:** ~80 lines → **~2 pages**

---

### C7. Remove Pretraining Objective Re-Explanations from Ch20

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** Ch20 Pretraining Strategies (lines 22–95, ~75 lines) re-explains CLM, MLM, span corruption, and denoising objectives — including formulas and derivations — that were already covered in their dedicated chapters: MLM in Ch13, CLM in Ch14, span corruption and denoising in Ch15.

**Proposal:** Replace with concise 1-line summaries referencing Ch13/14/15.

**Estimated savings:** ~50 lines → **~1 page**

---

### C8. Remove Mixed Precision / Gradient Checkpointing / ZeRO Re-Explanation from Ch20

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** Ch20 (lines 422–455, ~35 lines) re-explains mixed precision, gradient checkpointing, and ZeRO that are already covered in full detail in Ch11.

**Proposal:** Replace with a 3-line reference to Ch11.

**Estimated savings:** ~30 lines → **~1 page**

---

## Category D: Minor Cleanups

---

### D1. Fix Calculation Error in Ch7

**Status:** [x] IMPLEMENTED (included in B6)

**Problem:** Ch7 line 690 contains a self-noted calculation error: "wait, that's wrong. Let me recalculate" — this appears to be a draft artifact that was never cleaned up.

**Proposal:** Fix or remove the erroneous calculation.

**Estimated savings:** Negligible lines, but important for quality.

---

### D2. Fix Duplicate Subsection Header in Ch28

**Status:** [x] IMPLEMENTED (included in B14)

**Problem:** Ch28 lines 264 and 266 both declare `\subsection{Type Constraints}` — a copy-paste error.

**Proposal:** Remove the duplicate.

**Estimated savings:** 1 line.

---

### D3. Remove Speculative Model Claims from Ch19

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** Ch19 (lines 399–409) contains specific claims about proprietary model context lengths ("GPT-4 supports 128k tokens, Claude supports 200k tokens") and speculation about their implementation. These are already outdated and will continue to date.

**Proposal:** Either remove or convert to a footnote noting these were current as of a specific date.

**Estimated savings:** ~10 lines → negligible pages, but improves longevity.

---

### D4. Remove LoRA Mention from Ch1

**Status:** [ ] APPROVE / [ ] REJECT

**Problem:** Ch1 Linear Algebra (lines 466–469) mentions LoRA as an application of low-rank approximation. While mathematically relevant, LoRA is a fine-tuning technique that is more naturally placed in Ch20 (Pretraining Strategies) where it is properly contextualized.

**Proposal:** Remove or reduce to a single forward-reference sentence.

**Estimated savings:** ~3 lines — negligible, but reduces out-of-context references.

---

## Summary Table

| ID | Description | Est. Pages Saved | Category |
|----|-------------|-----------------|----------|
| **A1** | Consolidate drift/continuous learning into Ch24 | 20–25 | Structural |
| **A2** | Cut solutions 50–60% in Ch10–20 | 80–100 | Structural |
| **A3** | Cut solutions 40–50% in Ch1–9 | 6–8 | Structural |
| **A4** | Cut solutions 40–50% in Ch21–34 | 8–10 | Structural |
| **A5** | Consolidate hardware analysis into Ch12/Ch22 | 10–15 | Structural |
| **A6** | Eliminate triple coverage in Ch21/22/23 | 8–10 | Structural |
| **A7** | Consolidate BERT-base calculations | 5–7 | Structural |
| **B1** | Condense Ch11 training costs + recipe | 5–6 | Verbosity |
| **B2** | Condense Ch2 Adam + hardware sections | 4 | Verbosity |
| **B3** | Remove hardware tangent from Ch3 | 2–3 | Verbosity |
| **B4** | Trim hardware from Ch4 | 2 | Verbosity |
| **B5** | Move ViT comparison out of Ch5 | 2 | Verbosity |
| **B6** | Remove duplicates from Ch7 | 2–3 | Verbosity |
| **B7** | Remove self-duplicated T5 sizes in Ch15 | 1 | Verbosity |
| **B8** | Condense Ch18 fusion + computational | 2 | Verbosity |
| **B9** | Remove premature analysis from Ch10 | 4 | Verbosity |
| **B10** | Remove redundant 2nd implementation in Ch21 | 5–6 | Verbosity |
| **B11** | Remove "in Practice" restatements in Ch22 | 1 | Verbosity |
| **B12** | Restructure Ch23 as decision guide | 6–8 | Verbosity |
| **B13** | Trim RNN vs Transformer in Ch6 | 1 | Verbosity |
| **B14** | Tighten Ch28 case study + connections | 1–2 | Verbosity |
| **B15** | Reduce Ch31 drift from 33% to ~10% | 2–3* | Verbosity |
| **C1** | Remove Longformer/BigBird duplication (Ch16/19) | 1 | Duplicate |
| **C2** | Remove efficient attention preview from Ch8 | 1 | Duplicate |
| **C3** | Remove scoring re-listing from Ch9 | 0.5 | Duplicate |
| **C4** | Consolidate GPT-3 costs into Ch11 | 2 | Duplicate |
| **C5** | Consolidate scaling laws into Ch14 | 1 | Duplicate |
| **C6** | Consolidate KV caching into Ch14 | 2 | Duplicate |
| **C7** | Remove pretraining re-explanations from Ch20 | 1 | Duplicate |
| **C8** | Remove training technique re-explanations from Ch20 | 1 | Duplicate |
| **D1** | Fix calculation error in Ch7 | 0 | Cleanup |
| **D2** | Fix duplicate subsection in Ch28 | 0 | Cleanup |
| **D3** | Remove speculative claims from Ch19 | 0 | Cleanup |
| **D4** | Remove LoRA from Ch1 | 0 | Cleanup |

*B15 savings included in A1 estimate.

**Grand total (if all approved): ~220–270 pages**

Note: Some proposals overlap (e.g., A5 and B3/B4 both address hardware analysis in early chapters). The grand total accounts for this by not double-counting — individual estimates are net of overlap.
