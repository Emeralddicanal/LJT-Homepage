import urllib.request
import urllib.parse
import json
import base64
import os
import sys
import subprocess

# Try to get the GitHub token
token = os.environ.get('GITHUB_TOKEN', '')
if not token:
    # Try to get from git credential helper
    try:
        result = subprocess.run(
            ['git', 'config', '--global', 'github.token'],
            capture_output=True, text=True
        )
        token = result.stdout.strip()
    except:
        pass

if not token:
    # Try to get from git credentials
    try:
        result = subprocess.run(
            ['git', 'credential', 'fill'],
            input='protocol=https\nhost=github.com\n\n',
            capture_output=True, text=True
        )
        for line in result.stdout.split('\n'):
            if line.startswith('password='):
                token = line.split('=', 1)[1]
                break
    except:
        pass

if not token:
    print("No GitHub token found")
    sys.exit(1)

print(f"Token found, length: {len(token)}")

# Try to create a blob using the Git Data API
url = "https://api.github.com/repos/Emeralddicanal/LJT-Homepage/git/blobs"

# Test with simple content first
content = "Hello, World!"
data = {
    "content": base64.b64encode(content.encode()).decode(),
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
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"Blob created: {result['sha']}")
        print(f"URL: {result['url']}")
except Exception as e:
    print(f"Error: {e}")
