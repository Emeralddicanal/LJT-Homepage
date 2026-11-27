import urllib.request, json, base64, os, sys, subprocess

# Try to get token from various sources
token = ''
for cmd in [
    ['git', 'config', '--global', 'github.token'],
    ['git', 'config', 'github.token'],
]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.stdout.strip():
            token = r.stdout.strip()
            break
    except:
        pass

if not token:
    for key in ['GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_PAT']:
        token = os.environ.get(key, '')
        if token:
            break

print(f"Token found: {bool(token)}, length: {len(token)}")

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
