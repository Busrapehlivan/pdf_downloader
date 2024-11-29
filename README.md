
# Multi-Agent-AI-System-for-Collaborative-Task-Completion
=======
# Multi-Agent PDF Downloader

This project implements a multi-agent system using AutoGen for collaborative PDF downloading of academic papers. The system consists of multiple AI agents working together to search, download, and verify academic papers on a specified topic.

## Agents

1. **User Proxy Agent**: Coordinates the overall task and manages communication between agents
2. **Research Assistant**: Searches for relevant PDF papers using Google Scholar
3. **Download Manager**: Handles the downloading and proper storage of PDFs
4. **Quality Control**: Verifies downloads and ensures content relevance

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the script with:
```bash
python pdf_downloader.py
```

By default, it will search for papers about "machine learning optimization algorithms". You can modify the topic in the script.

## Features

- Collaborative multi-agent system using AutoGen
- Academic paper search using Google Scholar
- Automated PDF downloading
- Quality control and verification
- Structured file organization


## Note

Please ensure you comply with the terms of service of academic paper repositories and respect copyright laws when downloading papers.

