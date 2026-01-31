const chapters = [
    { id: 'preface', title: 'Preface', part: 'Front Matter' },
    { id: 'notation', title: 'Notation and Conventions', part: 'Front Matter' },
    { id: 'chapter01_linear_algebra', title: 'Chapter 1: Linear Algebra for Deep Learning', part: 'Part I: Mathematical Foundations' },
    { id: 'chapter02_calculus_optimization', title: 'Chapter 2: Calculus and Optimization', part: 'Part I: Mathematical Foundations' },
    { id: 'chapter03_probability_information', title: 'Chapter 3: Probability and Information Theory', part: 'Part I: Mathematical Foundations' },
    { id: 'chapter04_feedforward_networks', title: 'Chapter 4: Feed-Forward Neural Networks', part: 'Part II: Neural Network Fundamentals' },
    { id: 'chapter05_convolutional_networks', title: 'Chapter 5: Convolutional Neural Networks', part: 'Part II: Neural Network Fundamentals' },
    { id: 'chapter06_recurrent_networks', title: 'Chapter 6: Recurrent Neural Networks', part: 'Part II: Neural Network Fundamentals' },
    { id: 'chapter07_attention_fundamentals', title: 'Chapter 7: Attention Mechanisms: Fundamentals', part: 'Part III: Attention Mechanisms' },
    { id: 'chapter08_self_attention', title: 'Chapter 8: Self-Attention and Multi-Head Attention', part: 'Part III: Attention Mechanisms' },
    { id: 'chapter09_attention_variants', title: 'Chapter 9: Attention Variants and Mechanisms', part: 'Part III: Attention Mechanisms' },
    { id: 'chapter10_transformer_model', title: 'Chapter 10: Transformer Model', part: 'Part IV: Transformer Architecture' },
    { id: 'chapter11_training_transformers', title: 'Chapter 11: Training Transformers', part: 'Part IV: Transformer Architecture' },
    { id: 'chapter12_computational_analysis', title: 'Chapter 12: Computational Analysis', part: 'Part IV: Transformer Architecture' },
    { id: 'chapter13_bert', title: 'Chapter 13: BERT', part: 'Part V: Modern Transformer Variants' },
    { id: 'chapter14_gpt', title: 'Chapter 14: GPT', part: 'Part V: Modern Transformer Variants' },
    { id: 'chapter15_t5_bart', title: 'Chapter 15: T5 and BART', part: 'Part V: Modern Transformer Variants' },
    { id: 'chapter16_efficient_transformers', title: 'Chapter 16: Efficient Transformers', part: 'Part V: Modern Transformer Variants' },
    { id: 'chapter17_vision_transformers', title: 'Chapter 17: Vision Transformers', part: 'Part VI: Advanced Topics' },
    { id: 'chapter18_multimodal_transformers', title: 'Chapter 18: Multimodal Transformers', part: 'Part VI: Advanced Topics' },
    { id: 'chapter19_long_context', title: 'Chapter 19: Long Context', part: 'Part VI: Advanced Topics' },
    { id: 'chapter20_pretraining_strategies', title: 'Chapter 20: Pretraining Strategies', part: 'Part VI: Advanced Topics' },
    { id: 'chapter21_pytorch_implementation', title: 'Chapter 21: PyTorch Implementation', part: 'Part VII: Practical Implementation' },
    { id: 'chapter22_hardware_optimization', title: 'Chapter 22: Hardware Optimization', part: 'Part VII: Practical Implementation' },
    { id: 'chapter23_best_practices', title: 'Chapter 23: Best Practices', part: 'Part VII: Practical Implementation' },
    { id: 'chapter24_domain_specific_models', title: 'Chapter 24: Domain-Specific Models', part: 'Part VIII: Domain Applications' },
    { id: 'chapter25_enterprise_nlp', title: 'Chapter 25: Enterprise NLP', part: 'Part VIII: Domain Applications' },
    { id: 'chapter26_code_language', title: 'Chapter 26: Code and Language Models', part: 'Part VIII: Domain Applications' },
    { id: 'chapter27_video_visual', title: 'Chapter 27: Video and Visual Understanding', part: 'Part VIII: Domain Applications' },
    { id: 'chapter28_knowledge_graphs', title: 'Chapter 28: Knowledge Graphs and Reasoning', part: 'Part VIII: Domain Applications' },
    { id: 'chapter29_recommendations', title: 'Chapter 29: Recommendation Systems', part: 'Part VIII: Domain Applications' },
    { id: 'chapter30_healthcare', title: 'Chapter 30: Healthcare Applications', part: 'Part IX: Industry Applications' },
    { id: 'chapter31_finance', title: 'Chapter 31: Financial Applications', part: 'Part IX: Industry Applications' },
    { id: 'chapter32_legal', title: 'Chapter 32: Legal and Compliance Applications', part: 'Part IX: Industry Applications' },
    { id: 'chapter33_observability', title: 'Chapter 33: Observability and Monitoring', part: 'Part X: Production Systems' },
    { id: 'chapter34_dsl_agents', title: 'Chapter 34: DSL and Agent Systems', part: 'Part X: Production Systems' }
];

function groupChaptersByPart(chapters) {
    const grouped = {};
    chapters.forEach(chapter => {
        if (!grouped[chapter.part]) {
            grouped[chapter.part] = [];
        }
        grouped[chapter.part].push(chapter);
    });
    return grouped;
}

console.log('Total chapters:', chapters.length);
console.log('\nGrouped by part:');
const grouped = groupChaptersByPart(chapters);
Object.entries(grouped).forEach(([part, chaps]) => {
    console.log(`\n${part}: ${chaps.length} chapters`);
    chaps.forEach(c => console.log(`  - ${c.title}`));
});
