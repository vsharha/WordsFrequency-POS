#!/usr/bin/env bash
set -euxo pipefail

# Fetch repository info
for i in {1..2}
do
  curl -s "https://api.github.com/orgs/unimorph/repos?per_page=100&page=$i"
done |
  jq -r '.[] | select(.name | test("^[a-z]{3}$")) | "\(.name) \(.size)"' > unimorph_repos_with_size.txt

for i in {1..2}
do
  curl -s "https://api.github.com/orgs/unimorph/repos?per_page=100&page=$i"
done |
  grep ssh_url | 
  grep -o 'git@github.com:unimorph/[a-z]\{3\}.git' |
  sed 's/.*\/\([a-z]\{3\}\)\.git/\1/' > unimorph_repos.txt

python iso_639/check_iso_code.py --codes unimorph_repos.txt > validated_codes.txt

echo "Repository sizes for validated ISO codes:"
while read -r repo; do
  size_kb=$(curl -s "https://api.github.com/repos/unimorph/$repo" | jq -r '.size')
  if [ -n "$size_kb" ] && [ "$size_kb" != "null" ]; then
    size_gb=$(echo "scale=3; $size_kb / 1048576" | bc -l)
    size_mb=$(echo "scale=1; $size_kb / 1024" | bc -l)
    echo "$repo: ${size_mb} MB (${size_gb} GB)"
  else
    echo "$repo: Size not found"
  fi
done < validated_codes.txt
