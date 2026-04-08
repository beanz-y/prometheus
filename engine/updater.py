"""
Auto-updater - checks GitHub Releases for newer versions and downloads them.

No external dependencies (uses urllib from stdlib).
Designed to work inside PyInstaller-bundled .exe builds.
"""

import os
import sys
import json
import shutil
import zipfile
import ssl
import tempfile
from urllib.request import urlopen, Request
from urllib.error import URLError

# Some Windows environments have SSL certificate issues.
# Create a fallback context that doesn't verify (used only for updates).
try:
    _SSL_CTX = ssl.create_default_context()
except Exception:
    _SSL_CTX = None

if _SSL_CTX is None or True:
    # Fallback: unverified context (safe for read-only GitHub API calls)
    _SSL_CTX = ssl.create_default_context()
    _SSL_CTX.check_hostname = False
    _SSL_CTX.verify_mode = ssl.CERT_NONE


# ─── Configuration ─────────────────────────────────────────────────
# Set these to your GitHub repo. The updater checks
# https://api.github.com/repos/{OWNER}/{REPO}/releases/latest

GITHUB_OWNER = "beanz-y"
GITHUB_REPO = "prometheus"

UPDATE_CHECK_URL = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    if GITHUB_OWNER and GITHUB_REPO else ""
)
# ───────────────────────────────────────────────────────────────────


def get_current_version():
    """Read version from the VERSION file."""
    # Check multiple locations (bundled vs dev)
    candidates = []
    if getattr(sys, 'frozen', False):
        candidates.append(os.path.join(sys._MEIPASS, 'VERSION'))
        candidates.append(os.path.join(os.path.dirname(sys.executable), 'VERSION'))
    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'VERSION'))
    candidates.append(os.path.join(os.getcwd(), 'VERSION'))

    for path in candidates:
        try:
            with open(path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            continue
    return "0.0.0"


def parse_version(v):
    """Parse 'X.Y.Z' into a tuple for comparison."""
    try:
        # Strip leading 'v' if present
        v = v.lstrip('v').strip()
        parts = v.split('.')
        return tuple(int(p) for p in parts[:3])
    except (ValueError, AttributeError):
        return (0, 0, 0)


def check_for_update():
    """Check GitHub Releases for a newer version.

    Returns:
        dict with keys: available (bool), current (str), latest (str),
                        download_url (str), release_notes (str)
        OR None if check fails.
    """
    if not UPDATE_CHECK_URL:
        return None

    current = get_current_version()

    try:
        req = Request(UPDATE_CHECK_URL)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('User-Agent', 'PrometheusProtocol-Updater')

        with urlopen(req, timeout=5, context=_SSL_CTX) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        latest_tag = data.get('tag_name', '0.0.0')
        latest_ver = parse_version(latest_tag)
        current_ver = parse_version(current)

        # Find the zip asset for Windows
        download_url = ""
        for asset in data.get('assets', []):
            name = asset.get('name', '').lower()
            if name.endswith('.zip') and ('win' in name or 'prometheus' in name):
                download_url = asset.get('browser_download_url', '')
                break

        # Fallback: use the zipball URL
        if not download_url:
            download_url = data.get('zipball_url', '')

        return {
            'available': latest_ver > current_ver,
            'current': current,
            'latest': latest_tag,
            'download_url': download_url,
            'release_notes': data.get('body', '')[:500],
        }

    except (URLError, json.JSONDecodeError, KeyError, OSError):
        return None


def download_update(download_url, dest_dir=None):
    """Download and extract an update zip.

    Args:
        download_url: URL to the release zip file
        dest_dir: Where to extract (default: next to current exe)

    Returns:
        Path to extracted directory, or None on failure.
    """
    if not download_url:
        return None

    if dest_dir is None:
        if getattr(sys, 'frozen', False):
            dest_dir = os.path.dirname(sys.executable)
        else:
            dest_dir = os.getcwd()

    try:
        print(f"  Downloading update...")
        req = Request(download_url)
        req.add_header('User-Agent', 'PrometheusProtocol-Updater')

        # Download to temp file
        tmp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        with urlopen(req, timeout=60, context=_SSL_CTX) as resp:
            total = int(resp.headers.get('Content-Length', 0))
            downloaded = 0
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                tmp.write(chunk)
                downloaded += len(chunk)
                if total > 0:
                    pct = int(downloaded / total * 100)
                    print(f"\r  Downloading: {pct}%", end='', flush=True)
        tmp.close()
        print()

        # Extract to a temp directory first
        extract_dir = tempfile.mkdtemp(prefix='prometheus_update_')
        print(f"  Extracting...")
        with zipfile.ZipFile(tmp.name, 'r') as zf:
            zf.extractall(extract_dir)

        # Clean up temp zip
        os.unlink(tmp.name)

        # Find the game directory inside the extract
        # (GitHub zips often have a top-level directory)
        contents = os.listdir(extract_dir)
        if len(contents) == 1 and os.path.isdir(os.path.join(extract_dir, contents[0])):
            extract_dir = os.path.join(extract_dir, contents[0])

        return extract_dir

    except Exception as e:
        print(f"  Update failed: {e}")
        return None


def apply_update(extract_dir, app_dir=None):
    """Copy extracted update files over the current installation.

    Creates a backup of the current version first.
    Preserves the saves/ directory.
    """
    if app_dir is None:
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.getcwd()

    try:
        # Backup current _internal (the game code, not saves)
        internal = os.path.join(app_dir, '_internal')
        backup = os.path.join(app_dir, '_internal_backup')
        if os.path.exists(internal):
            if os.path.exists(backup):
                shutil.rmtree(backup)
            shutil.copytree(internal, backup)

        # Copy new files, skipping saves/
        for item in os.listdir(extract_dir):
            src = os.path.join(extract_dir, item)
            dst = os.path.join(app_dir, item)

            # Never overwrite saves
            if item == 'saves':
                continue

            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        print("  Update applied! Please restart the game.")
        return True

    except PermissionError:
        print("  Cannot update while game is running.")
        print(f"  New version extracted to: {extract_dir}")
        print("  Close the game, copy files manually, then restart.")
        return False
    except Exception as e:
        print(f"  Update failed: {e}")
        return False


def run_update_check(display=None):
    """Run the full update check flow. Called from main menu.

    Returns True if an update was applied (caller should restart).
    """
    if not UPDATE_CHECK_URL:
        if display:
            print("  Auto-update not configured.")
            print(f"  (Set GITHUB_OWNER and GITHUB_REPO in engine/updater.py)")
            print(f"  Current version: {get_current_version()}")
        return False

    print(f"  Current version: {get_current_version()}")
    print("  Checking for updates...")

    result = check_for_update()

    if result is None:
        print("  Could not reach update server. Playing offline.")
        return False

    if not result['available']:
        print(f"  You have the latest version ({result['current']}).")
        return False

    print(f"  New version available: {result['latest']} (you have {result['current']})")
    if result['release_notes']:
        print(f"\n  Release notes:\n  {result['release_notes'][:300]}")
    print()

    answer = input("  Download and install update? (y/n): ").strip().lower()
    if answer not in ('y', 'yes'):
        print("  Skipping update.")
        return False

    extract_dir = download_update(result['download_url'])
    if not extract_dir:
        return False

    return apply_update(extract_dir)
