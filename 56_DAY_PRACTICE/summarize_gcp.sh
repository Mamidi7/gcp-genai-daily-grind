#!/bin/bash
# Quick summarize for GCP docs
# Usage: ./summarize_gcp.sh <url> [short|medium|long]

export GEMINI_API_KEY="AIzaSyCov1Sacj-0M38aOe1Rx395oUCYWrzNWv0"

LENGTH=${2:-short}

echo "📝 Summarizing: $1"
echo "Length: $LENGTH"
echo "---"

summarize "$1" --model google/gemini-2.5-flash --length "$LENGTH"
