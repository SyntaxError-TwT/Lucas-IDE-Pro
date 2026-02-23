#!/bin/bash
echo "🚀 Lucas IDE Pro: Checking System Engines..."

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew (System Package Manager)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check and Install Languages
languages=("python" "rustc" "go" "java" "node")
for lang in "${languages[@]}"; do
    if ! command -v $lang &> /dev/null; then
        echo "Installing $lang..."
        brew install $lang
    else
        echo "✅ $lang is already installed."
    fi
done

# Setup Python Environment
pip3 install streamlit streamlit-ace pyflakes
streamlit run "Ultimate IDE Pro.py"