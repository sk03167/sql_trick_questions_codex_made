"""Vendor-specific REST extraction template. No real endpoint or token included.
Contract assumed: {"items": [...], "next_cursor": string-or-null}.
Call extract_pages with an authenticated fetch function and a staging directory.
A new run folder is required; on failure it contains partial pages, no manifest.
"""
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit

def fetch_page(endpoint, token, cursor, page_size=500, timeout=30, retries=4, sleep=time.sleep):
    if urlsplit(endpoint).scheme != "https" or urlsplit(endpoint).hostname != "api.example.invalid":
        raise ValueError("Replace the explicit endpoint allowlist for your vendor")
    query = {"page_size": page_size}
    if cursor is not None:
        query["cursor"] = cursor
    url = endpoint + "?" + urlencode(query)
    for attempt in range(retries + 1):
        request = Request(url, headers={"Authorization": "Bearer " + token, "Accept": "application/json"})
        try:
            with urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == retries:
                raise
            retry = exc.headers.get("Retry-After", "")
            # Seconds-only template. Adapt HTTP-date Retry-After and vendor policy.
            delay = min(120, float(retry)) if retry.isdigit() else min(30, 2 ** attempt)
            sleep(delay)
    raise RuntimeError("Unreachable retry state")

def extract_pages(fetch, directory, start_cursor=None, max_pages=100):
    if max_pages <= 0:
        raise ValueError("max_pages must be positive")
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=False)
    cursor, seen, files, total = start_cursor, set(), [], 0
    for page_index in range(max_pages):
        cursor_key = json.dumps(cursor, sort_keys=True)
        if cursor_key in seen:
            raise ValueError("Pagination cursor loop")
        seen.add(cursor_key)
        page = fetch(cursor)
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
            raise ValueError("Vendor response contract changed")
        if any(not isinstance(item, dict) for item in page["items"]):
            raise ValueError("Expected object records")
        name = f"page_{page_index:05d}.json"
        (root / name).write_text(''.join(json.dumps(item) + '\n' for item in page["items"]))
        files.append(name)
        total += len(page["items"])
        next_cursor = page.get("next_cursor")
        if next_cursor is None:
            manifest = {"complete": True, "files": files, "records": total,
                        "start_cursor": start_cursor, "next_cursor": None}
            (root / "manifest.json").write_text(json.dumps(manifest))
            return manifest
        if not isinstance(next_cursor, str) or not next_cursor:
            raise ValueError("Invalid next cursor")
        cursor = next_cursor
    raise RuntimeError("Page limit reached; no completion manifest")
# Land page files under a run folder that Auto Loader watches only after a
# completed manifest has been verified/moved by your ingestion controller.
# Do not point Auto Loader at an in-progress staging folder or at manifest JSON.
