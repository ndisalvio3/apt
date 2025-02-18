#!/usr/bin/env python3
import json
from pathlib import Path
import shutil
import requests
from sys import exit, argv

# Maximum number of packages to keep per source
MAX_PACKAGES = 3

# Determine the repository root (assumes this script is in the repo)
root = Path(__file__).parent

# Define the apt repository layout
debian = root / "debian"
pool_main = debian / "pool" / "main"
pool_main.mkdir(parents=True, exist_ok=True)

# The Packages file is expected in the standard location.
packages_file = debian / "dists" / "myrepo" / "main" / "binary-amd64" / "Packages"
if packages_file.exists():
    packages_content = packages_file.read_text()
else:
    packages_content = ""

def load_package_tracker(json_package_path: str) -> dict:
    """
    Load the JSON tracker file, creating it (and its parent directories)
    if it doesn't exist.
    """
    pkg_path = Path(json_package_path)
    if not pkg_path.exists():
        pkg_path.parent.mkdir(parents=True, exist_ok=True)
        with pkg_path.open("w") as f:
            json.dump({}, f, indent=2)
        return {}
    try:
        with pkg_path.open() as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def get_github_latest_deb(api_url: str) -> (str, str):
    """
    Retrieve the latest release info from GitHub and return a tuple:
    (filename, download_url) for the first asset ending with .deb.
    """
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    for asset in data.get("assets", []):
        if asset["name"].endswith(".deb"):
            return asset["name"], asset["browser_download_url"]
    raise Exception("No .deb asset found in the latest release from GitHub")

def missing_packages(base_url: str) -> bool:
    """
    Check if the package at base_url is missing from our Packages file,
    or if '--force' was passed on the command line.
    """
    # If the URL is from GitHub, use the GitHub API
    if "api.github.com/repos" in base_url:
        filename, _ = get_github_latest_deb(base_url)
    else:
        r = requests.get(base_url, allow_redirects=False)
        r.raise_for_status()
        final_url = r.headers.get("Location", base_url)
        filename = final_url.split("/")[-1]
    return filename not in packages_content or ("--force" in argv)

def get_all_packages(json_package_path: str, base_url: str) -> None:
    """
    For a given source (specified by its package tracker JSON and base_url),
    download any new package that isn't already tracked.
    """
    if "api.github.com/repos" in base_url:
        filename, final_url = get_github_latest_deb(base_url)
    else:
        r = requests.get(base_url, allow_redirects=False)
        r.raise_for_status()
        final_url = r.headers.get("Location", base_url)
        filename = final_url.split("/")[-1]

    # Load (or create) the JSON tracker file
    existing_packages = load_package_tracker(json_package_path)

    # If the package isn't in our global Packages content or if --force was given,
    # update the tracker.
    if filename not in packages_content or ("--force" in argv):
        existing_packages[filename] = final_url
        sorted_keys = sorted(existing_packages.keys())
        while len(existing_packages) > MAX_PACKAGES:
            oldest_key = sorted_keys.pop(0)
            del existing_packages[oldest_key]
        with Path(json_package_path).open("w") as f:
            json.dump(existing_packages, f, indent=2)
    
    # Download any package in our tracker that is not already in pool_main
    for pkg_name, pkg_url in existing_packages.items():
        local_path = pool_main / pkg_name
        if local_path.exists():
            continue
        print("Downloading", pkg_name, "from", pkg_url)
        with requests.get(pkg_url, stream=True) as r:
            r.raise_for_status()
            with local_path.open("wb") as f:
                shutil.copyfileobj(r.raw, f)

def main():
    # Load sources from sources.json
    sources_json = root / "sources.json"
    if not sources_json.exists():
        print("sources.json not found!")
        exit(1)
    with sources_json.open() as f:
        data = json.load(f)

    repos = data.get("repos", [])
    if not repos:
        print("No repos found in sources.json")
        exit(1)

    # Check if any packages are missing
    any_missing = False
    for repo in repos:
        if missing_packages(repo["url"]):
            any_missing = True

    if not any_missing:
        print("All packages already downloaded.")
        exit(0)

    print("Downloading new packages...")
    for repo in repos:
        get_all_packages(repo["package_json"], repo["url"])

if __name__ == "__main__":
    main()