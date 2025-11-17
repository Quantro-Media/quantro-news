import os
import re
import datetime

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "post"

def save_post(markdown_text, posts_dir="posts"):
    os.makedirs(posts_dir, exist_ok=True)

    # Find title in frontmatter
    match = re.search(r'^title:\s*"(.*?)"|^title:\s*(.*)$', markdown_text, re.MULTILINE)
    if match:
        title = (match.group(1) or match.group(2) or "post").strip()
    else:
        title = "post"

    fname = f"{datetime.date.today().isoformat()}-{slugify(title)}.md"
    path = os.path.join(posts_dir, fname)

    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    return path
