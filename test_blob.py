import urllib.request, json, base64, os, sys, subprocess

# Try to get token from various sources
token = os.environ.get('GITHUB_TOKEN', '')
if not token:
    token = os.environ.get('GH_TOKEN', '')
if not token:
    token = os.environ.get('GITHUB_PAT', '')

# Try git credential helper
if not token:
    try:
        result = subprocess.run(
            ['git', 'config', '--global', 'github.token'],
            capture_output=True, text=True
        )
        token = result.stdout.strip()
    except:
        pass

print(f"Token found: {bool(token)}, length: {len(token)}")

if token:
    # Try to create a blob using the Git Data API
    req = urllib.request.Request(
        "https://api.github.com/repos/Emeralddicanal/LJT-Homepage/git/blobs",
        data=json.dumps({"content": base64.b64encode(b"test content").decode(), "encoding": "base64"}).encode(),
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            print(f"Blob created: {data['sha']}")
    except Exception as e:
        print(f"Error: {e}")
