import urllib.request
import urllib.parse
import json
import base64
import os
import sys

# Try to get the GitHub token from the environment
token = os.environ.get('GITHUB_TOKEN', '')
if not token:
    # Try to read from git config
    import subprocess
    try:
        result = subprocess.run(['git', 'config', '--global', 'github.token'], capture_output=True, text=True)
        token = result.stdout.strip()
    except:
        pass

if not token:
    print("No GitHub token found")
    sys.exit(1)

print(f"Token found, length: {len(token)}")

# Now let's try to create a blob using the Git Data API
url = "https://api.github.com/repos/Emeralddicanal/LJT-Homepage/git/blobs"

# Test with a simple blob first
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
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"Blob created: {result['sha']}")
        print(f"URL: {result['url']}")
except Exception as e:
    print(f"Error: {e}")
