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
    # Try environment
    for key in ['GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_PAT']:
        token = os.environ.get(key, '')
        if token:
            break

print(f"Token found: {bool(token)}, length: {len(token)}")
