import yaml
from scripts.scrape import fetch_rss, fetch_web
from scripts.analyze_write import draft_post
from scripts.publish import save_post

def main():
    # Load config
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    niche = cfg.get("niche", "general")
    rss_urls = cfg.get("sources", {}).get("rss", [])
    web_urls = cfg.get("sources", {}).get("web", [])

    print("📡 Fetching sources...")
    rss_items = fetch_rss(rss_urls)
    web_items = fetch_web(web_urls)

    items = (rss_items + web_items)[:20]
    if not items:
        print("No items found. Check your config sources.")
        return

    print(f"🧠 Drafting post for niche: {niche} ...")
    md = draft_post(niche, items)

    print("💾 Saving post...")
    path = save_post(md)
    print(f"✅ Post saved at: {path}")

if __name__ == "__main__":
    main()
