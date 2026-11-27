import urllib.request
import json
import base64

# Test with a larger file
content = "x" * 50000
print(f"Content size: {len(content)} bytes")

# Try to create a blob using the Git Data API
# First, we need to get the current commit SHA
import subprocess
result = subprocess.run(
    ["curl", "-s", "-H", "Authorization: token " + open("/tmp/gh_token").read().strip(),
     "https://api.github.com/repos/Emeralddicanal/LJT-Homepage/git/ref/heads/master"],
    capture_output=True, text=True
)
print(result.stdout[:500])
