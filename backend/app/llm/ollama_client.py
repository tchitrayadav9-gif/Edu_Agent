"""
Ollama Local LLM Client.
Enables running private, offline LLMs (e.g. Llama 3, Mistral, DeepSeek-R1, Phi-3) via local Ollama daemon.
"""

import os
import httpx
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger("edumind.llm.ollama")


class OllamaClient:
    """HTTP Client for interacting with local Ollama instance."""
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3:latest")
        self.timeout = 60.0

    async def check_health(self) -> Dict[str, Any]:
        """Check if Ollama server is running locally and list available models."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("name") for m in data.get("models", [])]
                    return {
                        "is_running": True,
                        "base_url": self.base_url,
                        "available_models": models,
                        "selected_model": self.model
                    }
        except Exception as e:
            logger.debug(f"Ollama not reachable at {self.base_url}: {e}")
        
        return {
            "is_running": False,
            "base_url": self.base_url,
            "available_models": [],
            "selected_model": self.model,
            "setup_instructions": (
                "To run Ollama locally: 1. Download & install from https://ollama.com\n"
                "2. Run 'ollama run llama3' in your terminal\n"
                "3. Ensure the daemon is running on http://localhost:11434"
            )
        }

    async def generate_completion(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> Optional[str]:
        """Send a completion request to Ollama."""
        target_model = model or self.model
        payload = {
            "model": target_model,
            "prompt": prompt,
            "system": system or "",
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(f"{self.base_url}/api/generate", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data.get("response", "").strip()
                else:
                    logger.warning(f"Ollama returned status {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"Ollama generation failed: {e}")
        
        return None


# Global ollama client instance
ollama_client = OllamaClient()
