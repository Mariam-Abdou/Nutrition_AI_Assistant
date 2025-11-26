# Nutrition AI Assistant

An AI-powered diet planning assistant built with **Meta Llama 3.1 8B**, **LangChain**, and **RAG (Retrieval-Augmented Generation)**.
Ask questions about your personalized diet plan and get intelligent, context-aware responses.

## Features

- **AI-Powered Responses** - Uses Meta Llama 3.1 8B for intelligent answers
- **RAG Architecture** - Retrieves relevant information from diet plan using FAISS vector database
- **Smart Routing** - Automatically detects whether to use plan data or general knowledge
- **Natural Conversations** - Clean, human-friendly responses (no JSON!)
- **Context-Aware** - Understands portions, ingredients, and meal timing
- **Upload New Plans** - Dynamically update diet plans via PDF upload
- **REST API** - FastAPI backend with full documentation
- **UI** - Streamlit-based chat interface

### Chat Interface
```
👤 You: What should I eat for day 1 breakfast?

🤖 Assistant: DOCUMENT ✅HIGH-Confidence

For day 1 breakfast, you should have Greek yogurt with blueberries 
and almonds, along with coffee.

Food Items:
• low-fat plain Greek yogurt (6oz)
• ¾ cup blueberries
• 12 almonds or 2 tablespoons ground flaxseed meal
• coffee with milk and sugar substitute

Source: Day 1: Breakfast
```

## Architecture

```
┌────────────────────┐
│ Streamlit Frontend │  User Interface
│ (streamlit_app.py) │
└─────────┬──────────┘
          ↓  HTTP Requests
┌────────────────────┐
│   Ngrok Tunnel     │  Public Access
└─────────┬──────────┘
          ↓
┌────────────────────┐
│  FastAPI Backend   │  API Server
│  (Kaggle Notebook) │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│  Smart Router      │  Query
│ (DOCUMENT/GENERAL/ │  Classification
│     DEFAULT)       │
└─────────┬──────────┘
     ┌────┴────┐ 
     ↓         ↓  Route 
┌───────┐  ┌───────┐
│  RAG  │  │       │
│   +   │  │  LLM  │
│  LLM  │  │       │
└───────┘  └───────┘

Routing Logic
- DOCUMENT Mode: Questions about the diet plan (meals, days, ingredients, ...)
- GENERAL Mode: General nutrition questions (benefits, recipes, calories, ...)
- DEFAULT Mode: Checks plan first, uses general knowledge if no information in the plan.
``` 

## Technologies Used

### Core AI & Backend
- **Meta Llama 3.1 8B** - Large Language Model
- **LangChain** - LLM orchestration framework
- **FAISS** - Vector database for semantic search
- **intfloat/e5-large-v2** — Embedding model  
- **HuggingFace Transformers** - Model loading and inference
- **FastAPI** - REST API framework
- **Uvicorn** - ASGI server
- **BitsAndBytes** - 4-bit quantization for efficient inference

### Frontend
- **Streamlit** - Web interface
- **Requests** - HTTP client

### Infrastructure
- **Kaggle** - Free GPU compute
- **Ngrok** - Public tunnel for API access
- **PyPDF** - PDF parsing
