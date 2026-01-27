const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  const { id } = req.query;
  
  // Try multiple possible locations for chapter files
  const possiblePaths = [
    path.join(process.cwd(), 'public', 'chapters', `${id}.html`),
    path.join(process.cwd(), 'nodejs-version', 'public', 'chapters', `${id}.html`),
    path.join(__dirname, '..', '..', 'public', 'chapters', `${id}.html`),
    path.join(__dirname, '..', 'chapters', `${id}.html`)
  ];
  
  let foundPath = null;
  for (const testPath of possiblePaths) {
    if (fs.existsSync(testPath)) {
      foundPath = testPath;
      break;
    }
  }
  
  if (!foundPath) {
    return res.status(404).json({ 
      error: 'Chapter not found',
      id,
      triedPaths: possiblePaths,
      dirname: __dirname,
      cwd: process.cwd()
    });
  }
  
  fs.readFile(foundPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Error reading chapter', details: err.message });
    }
    
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=0, must-revalidate');
    res.send(data);
  });
};
