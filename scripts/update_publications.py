import os
import re
import requests
import yaml

ORCID_ID = "0000-0003-1091-6349"
PUB_DIR = "content/publication"

def clean_slug(title):
    return re.sub(r'[^a-zA-Z0-9_-]', '', title.lower().replace(' ', '-'))[:45]

def extract_doi_string(raw_doi):
    if not raw_doi:
        return ""
    # Normalize DOI string (lowercase, remove url prefix)
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', raw_doi.strip().lower())
    return doi

def get_existing_records():
    """Scans all existing publications to prevent duplicates and overwrites."""
    existing_dois = set()
    existing_titles = set()
    existing_folders = set()

    if not os.path.exists(PUB_DIR):
        return existing_dois, existing_titles, existing_folders

    for entry in os.listdir(PUB_DIR):
        entry_path = os.path.join(PUB_DIR, entry)
        if os.path.isdir(entry_path):
            existing_folders.add(entry)
            index_path = os.path.join(entry_path, "index.md")
            if os.path.exists(index_path):
                try:
                    with open(index_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Extract YAML frontmatter
                    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                    if match:
                        data = yaml.safe_load(match.group(1))
                        if isinstance(data, dict):
                            if "doi" in data and data["doi"]:
                                existing_dois.add(extract_doi_string(str(data["doi"])))
                            if "title" in data and data["title"]:
                                existing_titles.add(re.sub(r'\W+', '', data["title"].lower()))
                except Exception:
                    pass
    return existing_dois, existing_titles, existing_folders

def get_orcid_dois():
    url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return []

    dois = []
    data = r.json()
    for group in data.get("group", []):
        for summary in group.get("work-summary", []):
            ext_ids = summary.get("external-ids", {}).get("external-id", [])
            for ext in ext_ids:
                if ext.get("external-id-type") == "doi":
                    dois.append(ext.get("external-id-value").strip())
    return list(set(dois))

def fetch_csl_json(doi):
    headers = {"Accept": "application/vnd.citationstyles.csl+json"}
    r = requests.get(f"https://doi.org/{doi}", headers=headers)
    return r.json() if r.status_code == 200 else None

def sync():
    os.makedirs(PUB_DIR, exist_ok=True)
    existing_dois, existing_titles, existing_folders = get_existing_records()
    orcid_dois = get_orcid_dois()

    for doi in orcid_dois:
        normalized_doi = extract_doi_string(doi)
        if normalized_doi in existing_dois:
            continue  # DOI already exists; skip safely

        data = fetch_csl_json(doi)
        if not data:
            continue

        title = data.get("title", "").strip()
        normalized_title = re.sub(r'\W+', '', title.lower())
        if normalized_title in existing_titles:
            continue  # Title already exists under another folder; skip safely

        slug = clean_slug(title)
        if slug in existing_folders:
            continue

        authors = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in data.get("author", [])]
        date_parts = data.get("issued", {}).get("date-parts", [[2026, 1, 1]])[0]
        date_str = f"{date_parts[0]}-{date_parts[1] if len(date_parts) > 1 else 1:02d}-01"

        frontmatter = {
            "title": title,
            "authors": authors,
            "date": date_str,
            "doi": f"https://doi.org/{normalized_doi}",
            "publication": data.get("container-title", ""),
            "publication_types": ["2"],
            "abstract": data.get("abstract", "")
        }

        folder_path = os.path.join(PUB_DIR, slug)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "index.md")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml.dump(frontmatter, sort_keys=False))
            f.write("---\n")
        print(f"Safe addition: Created bundle for '{title}'")

if __name__ == "__main__":
    sync()
