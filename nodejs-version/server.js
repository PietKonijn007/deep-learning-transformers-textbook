const express = require('express');
const compression = require('compression');
const path = require('path');
const fs = require('fs');

const app = express();

// Enable gzip compression for faster loading
app.use(compression());

// Serve static files with caching
app.use(express.static('public', {
  maxAge: '1d',
  etag: true
}));

// API endpoint to get chapter list
app.get('/api/chapters', (req, res) => {
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
    { id: 'chapter23_best_practices', title: 'Chapter 23: Best Practices', part: 'Part VII: Practical Implementation' }
  ];
  res.json(chapters);
});

// API endpoint to get chapter content
app.get('/api/chapter/:id', (req, res) => {
  const chapterId = req.params.id;
  // Read from public/chapters directory (works for both local and Vercel)
  const htmlPath = path.join(__dirname, 'public', 'chapters', `${chapterId}.html`);
  
  fs.readFile(htmlPath, 'utf8', (err, data) => {
    if (err) {
      console.error(`Error reading chapter ${chapterId}:`, err);
      return res.status(404).json({ error: 'Chapter not found' });
    }
    // Ensure HTML content type
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.send(data);
  });
});

// Serve the main app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Export the app for Vercel
module.exports = app;

// Start server if running locally (not in Vercel)
if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`📚 Deep Learning & Transformers Book Server running on http://localhost:${PORT}`);
    console.log(`🚀 Fast loading with compression enabled`);
  });
}
