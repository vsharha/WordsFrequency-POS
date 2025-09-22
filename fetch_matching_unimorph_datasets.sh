#!/usr/bin/env bash
set -euxo pipefail

for i in {1..2}
do
  curl -s "https://api.github.com/orgs/unimorph/repos?per_page=100&page=$i"
done |
  grep ssh_url | 
  grep -o 'git@github.com:unimorph/[a-z]\{3\}.git' |
  sed 's/.*\/\([a-z]\{3\}\)\.git/\1/' > unimorph_repos.txt

  python iso_639/check_iso_code.py --codes unimorph_repos.txt > validated_codes.txt

  cat validated_codes.txt | xargs -I@ bash -c "git clone @; sleep 5"
