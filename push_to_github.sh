#!/bin/bash

echo "========================================"
echo "   GITHUB REPOSITORY PUSH SCRIPT"
echo "========================================"
echo ""

# Step 1: First create the repository on GitHub
echo "STEP 1: Create repository on GitHub"
echo "----------------------------------------"
echo "Please go to: https://github.com/new"
echo "Create a new repository named: business-voice-system"
echo "Make it Public or Private as you prefer"
echo "DO NOT initialize with README, .gitignore, or license"
echo ""
read -p "Press Enter when you've created the repository..."

# Step 2: Configure git (if needed)
echo ""
echo "STEP 2: Configuring Git..."
echo "----------------------------------------"
git config --global user.name "mansi936"
git config --global user.email "your-email@example.com"

# Step 3: Remove old remote and add new one
echo ""
echo "STEP 3: Setting up remote repository..."
echo "----------------------------------------"
git remote remove origin 2>/dev/null
git remote add origin https://github.com/mansi936/business-voice-system.git

# Step 4: Push the code
echo ""
echo "STEP 4: Pushing code to GitHub..."
echo "----------------------------------------"
git branch -M main
git push -u origin main

echo ""
echo "========================================"
echo "   PUSH COMPLETE!"
echo "========================================"
echo "Your repository is now available at:"
echo "https://github.com/mansi936/business-voice-system"
echo ""