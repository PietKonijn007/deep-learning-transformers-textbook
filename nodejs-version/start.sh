#!/bin/bash

echo "🚀 Starting Deep Learning & Transformers Interactive Book..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

echo "✅ Starting server..."
echo "📚 Open your browser to: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm start
