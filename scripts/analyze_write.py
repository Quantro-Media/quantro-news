import datetime
import frontmatter
import yaml
from scripts.ollama_client import generate

INSIGHT_PROMPT = """You are an expert market analyst.
You will be given a list of sources (titles, links, and short summaries).

Niche: {niche}

Write a clear, structured market brief with the following sections:
1. A strong title on the first line.
2. A 4–6 sentence executive summary.
3. 3–6 key trends as bullet points (with short explanations).
4. 2–3 concrete opportunities or action ideas.
5. A short closing outlook (2–3 sentences).

Rules:
- Use professional but readable language.
- Reference sources by their title or site (e.g. 'a recent report from ...').
- Aim for 700–1000 words.

SOURCES:
{sources}
"""

def build_sources_block(items):
    lines = []
    for i, it in enumerate(items, start=1):
        title = (it.get("title") or it.get("link") or "")[:160]
        summary = (it.get("summary") or "")[:300]
        link = it.get("link") or ""
        lines.append(f"{i}. {title}\n{link}\n{summary}\n")
    return "\n".join(lines)

def draft_post(niche, items):
    # Load footer config if exists
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    except Exception:
        cfg = {}

    sources_block = build_sources_block(items)
    prompt = INSIGHT_PROMPT.format(niche=niche, sources=sources_block)
    body = generate(prompt)

    # Try to extract the first non-empty line as the title
    first_line = ""
    for line in body.splitlines():
        stripped = line.strip("# ").strip()
        if stripped:
            first_line = stripped
            break
    if not first_line or len(first_line) > 140:
        first_line = f"{niche.title()} — Market Brief"

    # If the model starts with a generic phrase, override it
    lower = first_line.lower()
    if lower.startswith("as an expert market analyst") or lower.startswith("you are an expert market analyst"):
        first_line = f"{niche.title()} — Weekly Market Brief"

    # Append footer if enabled
    footer_cfg = (cfg or {}).get("footer", {})
    if footer_cfg.get("enabled") and footer_cfg.get("text"):
        body = body.rstrip() + "\n\n" + footer_cfg["text"].rstrip() + "\n"

    post = frontmatter.Post(body)
    post["title"] = first_line
    post["date"] = datetime.datetime.utcnow().isoformat() + "Z"
    post["niche"] = niche

    return frontmatter.dumps(post)

