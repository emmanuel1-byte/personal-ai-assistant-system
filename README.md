
---
# Personal AI Assistant   

This is the backend system for a **privacy-focused, voice-activated AI assistant** that automates personal and professional workflows. Built with **FastAPI**, it provides fast, secure, and scalable API endpoints for voice processing, task automation.

## Features  
- **Voice Command Processing** (Speech-to-Text, Wake-word detection)  
- **Task Automation** Email Summarization, Sending, Schedule Checking, and Call Scheduling  
- **Context-Aware AI Responses**  
- **Secure API Integrations** (Google)  

## Tech Stack  
- **Backend:** FastAPI (Python)  
- **AI & NLP:** OpenAI, Whisper, Coqui, Gemini  

## Setup  
1. Clone the repository:  
   ```sh
   git clone https://github.com/emmanuel1-byte/personal-ai-assistant-system.git 
   cd personal-ai-assistant-backend  
   ```  
2. Install dependencies:  
   ```sh
   poetry install
   ```  
3. Run the FastAPI server:  
   ```sh
   uvicorn main:app --reload  
   ```  

## API Documentation  
Once running, access the interactive API docs at:  
- **Swagger UI:** `http://127.0.0.1:8000/docs`  
- **ReDoc:** `http://127.0.0.1:8000/redoc`  

---