#!/usr/bin/env python3
import urllib.request, json, base64, os, sys, subprocess

# Try to get the GitHub token from various sources
token = os.environ.get('GITHUB_TOKEN', '')
if not token:
    token = os.environ.get('GH_TOKEN', '')
if not token:
    token = os.environ.get('GITHUB_PAT', '')
if not token:
    # Try git config
    try:
        result = subprocess.run(['git', 'config', '--global', 'github.token'], capture_output=True, text=True)
        token = result.stdout.strip()
    except:
        pass
if not token:
    try:
        result = subprocess.run(['git', 'config', 'github.token'], capture_output=True, text=True)
        token = result.stdout.strip()
    except:
        pass

print(f"Token found: {bool(token)}, length: {len(token)}")

if not token:
    sys.exit(1)

# Try to create a blob using the Git Data API
url = "https://api.github.com/repos/Emeralddicanal/LJT-Homepage/git/blobs"
data = {
    "content": base64.b64encode(b"Hello, World!").decode(),
    "encoding": "base64"
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode(),
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"Blob created: {result['sha']}")
        print(f"URL: {result['url']}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode())
except Exception as e:
    print(f"Error: {e}")
