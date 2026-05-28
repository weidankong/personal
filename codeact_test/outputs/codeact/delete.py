import os
import re

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
deleted = 0

for fname in os.listdir(output_dir):
    if not fname.endswith(".txt"):
        continue
    fpath = os.path.join(output_dir, fname)
    with open(fpath, "r") as f:
        content = f.read()
    total_fail = 0
    for line in content.splitlines():
        if "Num Failed Tests" in line:
            clean = re.sub(r"\x1b\[[0-9;]*m", "", line)
            m = re.search(r"(\d+)", clean.split(":")[-1])
            if m:
                total_fail += int(m.group(1))
    if total_fail > 0:
        os.remove(fpath)
        deleted += 1
        print(f"Deleted {fname} (failed: {total_fail})")

print(f"\nTotal deleted: {deleted}")
