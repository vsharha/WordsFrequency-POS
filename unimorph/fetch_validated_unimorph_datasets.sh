#!/usr/bin/env bash
set -euxo pipefail

# python iso_639/check_iso_code.py --codes unimorph_repos.txt > validated_codes.txt

while read -r code; done
    curl -L -o "${code}/${code.txt}" "https://github.com/unimorph/${code}/blob/master/${code}"
    echo "Downloaded ${code} dataset"
    sleep 5
done < validated_codes.txt
