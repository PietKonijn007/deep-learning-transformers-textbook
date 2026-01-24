#!/bin/bash

# Vercel Deployment Helper Script
# This script helps deploy the Deep Learning & Transformers textbook to Vercel

echo "🚀 Vercel Deployment Helper"
echo "============================"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found"
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Vercel CLI"
        echo "💡 Try: sudo npm install -g vercel"
        exit 1
    fi
fi

echo "✅ Vercel CLI found"
echo ""

# Check if we're in the right directory
if [ ! -f "server.js" ]; then
    echo "❌ Error: server.js not found"
    echo "💡 Please run this script from the nodejs-version directory"
    exit 1
fi

echo "✅ In correct directory"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

echo "✅ Dependencies installed"
echo ""

# Ask user what they want to do
echo "What would you like to do?"
echo "1) Deploy to preview (test deployment)"
echo "2) Deploy to production"
echo "3) Check deployment status"
echo "4) View logs"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Deploying to preview..."
        vercel
        ;;
    2)
        echo ""
        echo "🚀 Deploying to production..."
        vercel --prod
        ;;
    3)
        echo ""
        echo "📊 Checking deployment status..."
        vercel ls
        ;;
    4)
        echo ""
        echo "📋 Viewing logs..."
        vercel logs
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Done!"
