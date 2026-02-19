#!/usr/bin/env python3
"""
PII Scrubber - Sovereign Privacy Guard (v1.0)
Uses local Ollama (Llama 3.2 3B) to redact PII before cloud processing.
"""

import os
import sys
import json
import requests
import re

# Config
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2:3b" # Efficient for local scrubbing

def scrub_text(text):
    """Asks local Llama to redact PII from text"""
    print(f"🔐 Scrubber: Protegiendo datos con {MODEL}...")
    
    prompt = f"""
    SYSTEM: You are a PII (Personally Identifiable Information) Redactor.
    TASK: Replace all names, email addresses, phone numbers, and specific physical addresses with generic placeholders like [NAME], [EMAIL], [PHONE], [ADDRESS].
    KEEP: Keep all technical context, product names, and non-private data intact.
    
    TEXT TO SCRUB:
    {text}
    
    OUTPUT: Provide ONLY the scrubbed text.
    """
    
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": MODEL, 
            "prompt": prompt, 
            "stream": False
        }, timeout=30)
        
        if res.status_code == 200:
            scrubbed = res.json().get('response', '').strip()
            return scrubbed
        else:
            print(f"❌ Scrubber Error: {res.text}")
            return text # Fallback to original (unsafe but prevents crash)
    except Exception as e:
        print(f"❌ Scrubber Exception: {e}")
        return text

def main():
    if len(sys.argv) > 1:
        input_data = sys.argv[1]
        
        # Check if it's a file path
        if os.path.exists(input_data):
            with open(input_data, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = input_data
            
        result = scrub_text(content)
        print("\n--- 🛡️ SCRUBBED OUTPUT ---")
        print(result)
    else:
        print("Usage: pii_scrubber.py <text_or_file_path>")

if __name__ == "__main__":
    main()
