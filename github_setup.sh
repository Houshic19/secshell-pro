#!/bin/bash

# SecShell PRO - GitHub Setup Helper Script
# This script helps you push your code to GitHub

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  SecShell PRO - GitHub Repository Setup                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is configured
if git config --global user.name > /dev/null 2>&1; then
    echo "✓ Git user: $(git config --global user.name)"
else
    echo "⚠ Git user not configured. Run: git config --global user.name 'Your Name'"
fi

if git config --global user.email > /dev/null 2>&1; then
    echo "✓ Git email: $(git config --global user.email)"
else
    echo "⚠ Git email not configured. Run: git config --global user.email 'your@email.com'"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 1: Create GitHub Repository Manually"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Go to: https://github.com/new"
echo ""
echo "Fill in these details:"
echo "  Repository name: secshell-pro"
echo "  Description: Intelligent Security Automation Platform"
echo "  Privacy: Public (or Private if you prefer)"
echo "  DO NOT initialize with README, .gitignore, or license"
echo ""
echo "Click 'Create repository'"
echo ""

read -p "Press ENTER after creating the GitHub repository..."

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 2: Enter Your GitHub Username"
echo "════════════════════════════════════════════════════════════════"
echo ""

read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

REPO_URL="https://github.com/${github_username}/secshell-pro.git"

echo ""
echo "✓ Repository URL: $REPO_URL"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo "STEP 3: Configure Remote and Push"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "⚠ Remote 'origin' already exists"
    read -p "Do you want to update it? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin "$REPO_URL"
        echo "✓ Remote updated"
    fi
else
    git remote add origin "$REPO_URL"
    echo "✓ Remote added: origin -> $REPO_URL"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 4: Push to GitHub"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "You will be prompted to authenticate with GitHub."
echo "Use one of these methods:"
echo "  • GitHub personal access token (PAT)"
echo "  • GitHub CLI (gh auth login)"
echo "  • SSH key (if configured)"
echo ""

read -p "Ready to push? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing to GitHub..."
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║  ✅ SUCCESS! Code pushed to GitHub                            ║"
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo ""
        echo "Repository URL: https://github.com/${github_username}/secshell-pro"
        echo ""
        echo "Next steps:"
        echo "  1. Visit your repository on GitHub"
        echo "  2. Star ⭐ if you like it!"
        echo "  3. Share it with others"
        echo ""
    else
        echo "❌ Push failed. Common issues:"
        echo "  • Authentication failed - check your GitHub credentials"
        echo "  • Repository doesn't exist - verify it was created"
        echo "  • Permission denied - check SSH keys or PAT"
        echo ""
        echo "Manual push command:"
        echo "  git push -u origin main"
    fi
else
    echo "Push cancelled. You can manually push later with:"
    echo "  git push -u origin main"
fi
