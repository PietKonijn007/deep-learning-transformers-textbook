const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  const info = {
    dirname: __dirname,
    cwd: process.cwd(),
    nodeVersion: process.version,
    platform: process.platform,
    env: {
      VERCEL: process.env.VERCEL,
      VERCEL_ENV: process.env.VERCEL_ENV
    },
    paths: {}
  };
  
  // Check various paths
  const testPaths = [
    'public/chapters',
    '../public/chapters',
    'chapters',
    '../chapters'
  ];
  
  testPaths.forEach(p => {
    const fullPath = path.join(__dirname, p);
    try {
      const exists = fs.existsSync(fullPath);
      info.paths[p] = {
        fullPath,
        exists,
        files: exists ? fs.readdirSync(fullPath).slice(0, 5) : []
      };
    } catch (e) {
      info.paths[p] = { fullPath, error: e.message };
    }
  });
  
  res.json(info);
};
