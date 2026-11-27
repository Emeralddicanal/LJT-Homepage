import urllib.request
import urllib.parse
import json
import base64
import os
import sys
import subprocess

# Try to get the GitHub token from various sources
token = ''

# Try environment variables
for key in ['GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_PAT']:
    token = os.environ.get(key, '')
    if token:
        break

# Try git config
if not token:
    for cmd in [
        ['git', 'config', '--global', 'github.token'],
        ['git', 'config', 'github.token'],
    ]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                token = result.stdout.strip()
                break
        except:
            pass

print(f"Token found: {bool(token)}")
print(f"Token length: {len(token)}")

# Try to use the Git Data API to create a blob
if token:
    url = "https://api.github.com/repos/Emeralddicanal/LJT-Homepage/git/blobs"
    data = {
        "content": base64.b64encode(b"test content").decode(),
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
    except Exception as e:
        print(f"Error: {e}")
