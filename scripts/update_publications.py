import os
import re
import requests
import yaml

ORCID_ID = "0000-0003-1091-6349"
PUB_DIR = "content/publication"
USER_EMAIL = "S.A.Mitchell@bsms.ac.uk"  # Required for Unpaywall polite API pool

PREPRINT_DOI_PREFIXES = [
    "10.1101/",   # bioRxiv / medRxiv
    "10.21203/",  # Research Square
    "10.48550/",  # arXiv
    "10.20944/",  # Preprints.org
    "10.31219/",  # OSF Preprints
]

def clean_slug(title):
    return re.sub(r'[^a-zA-Z0-9_-]', '', title.lower().replace(' ', '-'))[:45]

def extract_doi_string(raw_doi):
    if not raw_doi:
        return ""
    return re.sub(r'^https?://(dx\.)?doi\.org/', '', raw_doi.strip().lower())

def determine_publication_type(doi, data):
    norm_doi = doi.lower()
    csl_type = data.get("type", "").lower()
    container = data.get("container-title", "").lower()
    publisher = data.get("publisher", "").lower()
    issue = str(data.get("issue", "")).lower()
    volume = str(data.get("volume", "")).lower()
    page = str(data.get("page", "")).lower()

    is_preprint = (
        any(norm_doi.startswith(prefix) for prefix in PREPRINT_DOI_PREFIXES)
        or csl_type in ["posted-content", "preprint"]
        or any(k in container for k in ["biorxiv", "medrxiv", "research square", "arxiv", "preprints"])
        or any(k in publisher for k in ["research square", "cold spring harbor"])
    )
    if is_preprint:
        pub_venue = data.get("container-title") or ("Research Square" if "10.21203" in norm_doi else "bioRxiv")
        return ["3"], pub_venue

    is_conference_abstract = (
        csl_type in ["proceedings-article", "paper-conference"]
        or "supplement" in issue
        or "supplement" in volume
        or "abstract" in page
        or "meeting abstract" in container
    )
    if is_conference_abstract:
        pub_venue = data.get("container-title", "")
        if issue and "supplement" in issue:
            pub_venue = f"{pub_venue} ({issue.title()})"
        return ["1"], pub_venue

    return ["2"], data.get("container-title", "")

def get_pdf_url(doi, csl_data):
    """Attempts to find an Open Access PDF URL via Unpaywall or Preprint links."""
    # 1. Try Unpaywall API
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email={USER_EMAIL}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            best_oa = r.json().get("best_oa_location")
            if best_oa and best_oa.get("url_for_pdf"):
                return best_oa.get("url_for_pdf")
    except Exception:
        pass

    # 2. Check bioRxiv direct PDF URL pattern
    if doi.startswith("10.1101/"):
        return f"https://www.biorxiv.org/content/{doi}.full.pdf"

    # 3. Check CSL resource link
    link = csl_data.get("link", [])
    for item in link:
        if item.get("content-type") == "application/pdf":
            return item.get("URL")

    return None

def download_pdf(pdf_url, target_path):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(pdf_url, headers=headers, stream=True, timeout=15)
        # Verify content type is actually PDF, not a paywall login page
        content_type = resp.headers.get("content-type", "").lower()
        if resp.status_code == 200 and ("pdf" in content_type or resp.content[:4] == b"%PDF"):
            with open(target_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception:
        pass
    return False

def get_existing_records():
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

    missing_pdfs = []

    for doi in orcid_dois:
        normalized_doi = extract_doi_string(doi)
        if normalized_doi in existing_dois:
            continue

        data = fetch_csl_json(doi)
        if not data:
            continue

        title = data.get("title", "").strip()
        normalized_title = re.sub(r'\W+', '', title.lower())
        if normalized_title in existing_titles:
            continue

        slug = clean_slug(title)
        if slug in existing_folders:
            continue

        authors = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in data.get("author", [])]
        date_parts = data.get("issued", {}).get("date-parts", [[2026, 1, 1]])[0]
        date_str = f"{date_parts[0]}-{date_parts[1] if len(date_parts) > 1 else 1:02d}-01"

        pub_type, venue = determine_publication_type(normalized_doi, data)

        frontmatter = {
            "title": title,
            "authors": authors,
            "date": date_str,
            "doi": f"https://doi.org/{normalized_doi}",
            "publication": venue,
            "publication_types": pub_type,
            "abstract": data.get("abstract", "")
        }

        folder_path = os.path.join(PUB_DIR, slug)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "index.md")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml.dump(frontmatter, sort_keys=False))
            f.write("---\n")

        # Attempt PDF download
        pdf_url = get_pdf_url(normalized_doi, data)
        # Wowchemy automatically recognizes featured.pdf in the bundle folder
        pdf_saved = False
        if pdf_url:
            pdf_path = os.path.join(folder_path, "featured.pdf")
            pdf_saved = download_pdf(pdf_url, pdf_path)

        if pdf_saved:
            print(f"Downloaded PDF for: {title}")
        else:
            missing_pdfs.append((title, folder_path))

        type_label = "Preprint" if pub_type == ["3"] else ("Conference Abstract" if pub_type == ["1"] else "Journal Article")
        print(f"Added [{type_label}]: {title}")

    # Write missing PDFs list for the GitHub PR description
    if missing_pdfs:
        with open("missing_pdfs.txt", "w", encoding="utf-8") as f:
            for item, path in missing_pdfs:
                f.write(f"- [ ] **Missing PDF:** *{item}* (Upload `featured.pdf` into `{path}`)\n")

if __name__ == "__main__":
    sync()
