import urllib.request
import urllib.parse
import json
import base64
import os
import sys
import subprocess

# Try to get token from git config
token = ''
for key in ['GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_PAT']:
    token = os.environ.get(key, '')
    if token:
        break

if not token:
    # Try to get from git config
    for cmd in [
        ['git', 'config', '--global', 'github.token'],
        ['git', 'config', 'github.token'],
    ]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                token = result.stdout.strip()
                break
        except Exception as e:
            print(f"Error running {' '.join(cmd)}: {e}")

print(f"Token found: {bool(token)}")
print(f"Token length: {len(token)}")

# Try to create a blob using the Git Data API
url = "https://api.github.com/repos/Emeralddicanal/LJT-Homepage/git/blobs"

# Test with simple content first
test_content = "Hello, World!"
data = {
    "content": base64.b64encode(test_content.encode()).decode(),
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
        response = json.loads(resp.read().decode())
        print(f"Blob created: {response['sha']}")
        print(f"URL: {response['url']}")
except Exception as e:
    print(f"Error: {e}")
