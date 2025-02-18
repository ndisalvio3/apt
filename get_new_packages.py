import json
from pathlib import Path
import shutil
import requests
from sys import exit, argv

# Constants
root = Path(__file__).parent
MAX_PACKAGES = 3

# Apt repo layout
debian_dir = root / "debian"
pool_main = debian_dir / "pool" / "main"
packages_file = debian_dir / "dists" / "myrepo" / "main" / "binary-amd64" / "Packages"

pool_main.mkdir(parents=True, exist_ok=True)
packages_file.parent.mkdir(parents=True, exist_ok=True)

if packages_file.exists():
    packages_content = packages_file.read_text()
else:
    packages_content = ""

def missing_packages(base_url: str) -> bool:
    """Check if the package from base_url is missing or if --force is given."""
    resp = requests.get(base_url, allow_redirects=False)
    resp.raise_for_status()
    final_url = resp.headers.get("Location", base_url)
    filename = final_url.split("/")[-1]
    return filename not in packages_content or ("--force" in argv)

def get_all_packages(json_package_path: str, base_url: str) -> None:
    """Download new package if missing, update the JSON tracker, store in pool/main."""
    resp = requests.get(base_url, allow_redirects=False)
    resp.raise_for_status()
    final_url = resp.headers.get("Location", base_url)
    filename = final_url.split("/")[-1]

    # Load existing JSON tracker (or start fresh if none)
    pkg_tracker = root / json_package_path
    if pkg_tracker.exists():
        with pkg_tracker.open() as f:
            existing_packages = json.load(f)
    else:
        existing_packages = {}

    # If missing or forced, record in JSON
    if filename not in packages_content or ("--force" in argv):
        existing_packages[filename] = final_url
        sorted_keys = sorted(existing_packages.keys())
        # Limit number of older packages
        while len(existing_packages) > MAX_PACKAGES:
            oldest_key = sorted_keys.pop(0)
            del existing_packages[oldest_key]

        with pkg_tracker.open("w") as f:
            json.dump(existing_packages, f, indent=2)

    # Download any new packages not in pool/main
    for pkg_name, pkg_url in existing_packages.items():
        local_path = pool_main / pkg_name
        if not local_path.exists():
            print(f"Downloading {pkg_name} from {pkg_url}")
            with requests.get(pkg_url, stream=True) as r:
                r.raise_for_status()
                with local_path.open("wb") as out:
                    shutil.copyfileobj(r.raw, out)

def main():
    # 1. Load all repos from sources.json
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

    # 2. Check if any packages are missing
    any_missing = False
    for repo in repos:
        if missing_packages(repo["url"]):
            any_missing = True

    if not any_missing:
        print("All packages already downloaded.")
        exit(0)

    print("Downloading new packages...")
    # 3. Download new packages for each repo
    for repo in repos:
        get_all_packages(repo["package_json"], repo["url"])

    # 4. (Optional) Rebuild the Packages file if you want
    #    e.g. using dpkg-scanpackages in a Makefile or here:
    # import subprocess
    # subprocess.run([
    #   "dpkg-scanpackages",
    #   pool_main.as_posix(),
    #   "/dev/null"
    # ], stdout=packages_file.open("w"))

if __name__ == "__main__":
    main()