# 📝 Summarize Tool - Quick Reference

## Installation
```bash
npm i -g @steipete/summarize
```

## Setup API Key
```bash
# Add to ~/.zshrc for persistent use
export GEMINI_API_KEY="AIzaSyCov1Sacj-0M38aOe1Rx395oUCYWrzNWv0"
```

## Daily Commands

### Quick Summary (GCP Docs)
```bash
summarize "https://cloud.google.com/vertex-ai/docs/..." --length short
summarize "URL" -s  # short
summarize "URL" -m  # medium
```

### Extract Content (No LLM)
```bash
summarize "URL" --extract
```

### YouTube Videos
```bash
summarize "https://youtube.com/watch?v=..." --length medium
summarize "yt-url" --slides  # Extract slides
```

### PDFs
```bash
summarize "/path/to/file.pdf" --length medium
```

### Use Specific Model
```bash
summarize "URL" --model google/gemini-2.5-flash
summarize "URL" --model openai/gpt-4o
```

## GCP-Specific Quick Commands

```bash
# Vertex AI
summarize "https://cloud.google.com/vertex-ai/docs" --length short

# BigQuery
summarize "https://cloud.google.com/bigquery/docs" --length short

# Gemini
summarize "https://cloud.google.com/generative-ai/docs" --length short

# LangChain
summarize "https://python.langchain.com/docs" --length short

# RAG
summarize "https://python.langchain.com/docs/rag" --length short
```

## Cost
- ~$0.007 per short summary
- ~$0.02 per medium summary
- Very cheap for research!

## Script Usage
```bash
# Quick GCP summary script
./summarize_gcp.sh "URL" short
```
