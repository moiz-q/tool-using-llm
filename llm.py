"""
LLM interface using Ollama.
Reused from llm-basics-playground.
"""

import requests
import time
from typing import Optional


def call_llm(
    prompt: str,
    model: str = "llama3.2",
    temperature: float = 0.0,
    max_retries: int = 3,
    json_mode: bool = False
) -> str:
    """
    Call Ollama LLM with retry logic.
    
    Args:
        prompt: The prompt to send
        model: Model name (default: llama3.2)
        temperature: 0.0 = deterministic, 1.0 = creative
        max_retries: Number of retry attempts
        json_mode: Request JSON output format
    
    Returns:
        Generated text response
    """
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
    }
    
    if json_mode:
        payload["format"] = "json"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result["response"].strip()
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise Exception(f"LLM call failed after {max_retries} attempts: {e}")
    
    return ""


if __name__ == "__main__":
    # Test
    response = call_llm("Say hello in one sentence.")
    print(response)
