import requests

def generate(prompt, model="llama3", temperature=0.7):
    """
    Call the local Ollama LLM and return the text response.
    Make sure `ollama serve` is running in another terminal.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "").strip()
