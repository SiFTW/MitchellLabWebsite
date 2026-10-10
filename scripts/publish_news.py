import os
import re
import sys
import datetime
import requests
import yaml

CONTENT_DIR = "content/event"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}

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
        # Captures markdown ![...](url), <img src="url">, or raw links
        url_match = re.search(r'https?://[^\s\)\"\'>]+', raw_img)
        if url_match:
            data["image_url"] = url_match.group(0)

    return data

def download_image(url, target_dir):
    """Downloads image and saves it as featured.jpg or featured.png."""
    try:
        session = requests.Session()
        # Optional: Pass GitHub token if downloading from private repository assets
        token = os.environ.get("GITHUB_TOKEN")
        headers = dict(HEADERS)
        if token and "github" in url:
            headers["Authorization"] = f"token {token}"

        r = session.get(url, headers=headers, stream=True, timeout=20, allow_redirects=True)
        if r.status_code == 200:
            content_type = r.headers.get("Content-Type", "").lower()
            if "png" in content_type:
                ext = ".png"
            elif "gif" in content_type:
                ext = ".gif"
            elif "webp" in content_type:
                ext = ".webp"
            else:
                ext = ".jpg"

            img_path = os.path.join(target_dir, f"featured{ext}")
            with open(img_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded image to {img_path}")
            return True
        else:
            print(f"Failed to fetch image: HTTP {r.status_code} from {url}")
    except Exception as e:
        print(f"Error fetching image: {e}")
    return False

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

    # Download image
    if news["image_url"]:
        print(f"Detected image URL: {news['image_url']}")
        saved = download_image(news["image_url"], bundle_dir)
        if saved:
            frontmatter["image"] = {"caption": "", "focal_point": "Smart"}

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
