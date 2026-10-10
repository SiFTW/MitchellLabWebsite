import os
import re
import sys
import datetime
import requests
import yaml

CONTENT_DIR = "content/event"

def clean_slug(title):
    slug = re.sub(r'[^a-zA-Z0-9_-]', '', title.lower().replace(' ', '-'))
    return slug[:50].strip('-')

def parse_issue(body):
    data = {"title": "", "date": "", "summary": "", "link": "", "image_url": ""}
    
    title_match = re.search(r'### News Title\s*\n\s*(.*?)(?=\n###|\Z)', body, re.DOTALL)
    if title_match:
        data["title"] = title_match.group(1).strip()

    date_match = re.search(r'### Date\s*\n\s*(.*?)(?=\n###|\Z)', body, re.DOTALL)
    if date_match:
        val = date_match.group(1).strip()
        if re.match(r'^\d{4}-\d{2}-\d{2}$', val):
            data["date"] = val

    summary_match = re.search(r'### Brief Summary / Blurb\s*\n\s*(.*?)(?=\n###|\Z)', body, re.DOTALL)
    if summary_match:
        data["summary"] = summary_match.group(1).strip()

    link_match = re.search(r'### External Link \(Read More\)\s*\n\s*(.*?)(?=\n###|\Z)', body, re.DOTALL)
    if link_match:
        data["link"] = link_match.group(1).strip()

    img_match = re.search(r'### Featured Image\s*\n\s*(.*?)(?=\n###|\Z)', body, re.DOTALL)
    if img_match:
        raw_img = img_match.group(1).strip()
        url_match = re.search(r'https?://[^\s\)]+', raw_img)
        if url_match:
            data["image_url"] = url_match.group(0)

    return data

def main():
    issue_body = os.environ.get("ISSUE_BODY", "")
    if not issue_body:
        sys.exit(0)

    news = parse_issue(issue_body)
    if not news["title"]:
        print("No title found, skipping.")
        sys.exit(0)

    slug = clean_slug(news["title"])
    bundle_dir = os.path.join(CONTENT_DIR, slug)
    os.makedirs(bundle_dir, exist_ok=True)

    # Use provided date if supplied, otherwise use UTC now
    now = datetime.datetime.now(datetime.timezone.utc)
    if news["date"]:
        date_str = f"{news['date']}T12:00:00Z"
    else:
        date_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    frontmatter = {
        "title": news["title"],
        "date": date_str,
        "publishDate": date_str,
        "summary": news["summary"],
        "authors": ["admin"],
        "all_day": False,
    }

    if news["link"]:
        frontmatter["links"] = [{
            "icon": "globe",
            "icon_pack": "fas",
            "name": "Read More",
            "url": news["link"]
        }]

    if news["image_url"]:
        try:
            r = requests.get(news["image_url"], timeout=15)
            if r.status_code == 200:
                ext = ".png" if "image/png" in r.headers.get("Content-Type", "") else ".jpg"
                img_path = os.path.join(bundle_dir, f"featured{ext}")
                with open(img_path, "wb") as f:
                    f.write(r.content)
                frontmatter["image"] = {"caption": "", "focal_point": "Smart"}
        except Exception as e:
            print(f"Warning: Failed to download image: {e}")

    md_content = "---\n"
    md_content += yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
    md_content += "---\n\n"
    md_content += f"{news['summary']}\n"
    if news["link"]:
        md_content += f"\n[Read more]({news['link']})\n"

    with open(os.path.join(bundle_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Published news item bundle: {bundle_dir}")

if __name__ == "__main__":
    main()
