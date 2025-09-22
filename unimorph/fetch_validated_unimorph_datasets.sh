#!/usr/bin/env bash
set -euxo pipefail

# python iso_639/check_iso_code.py --codes unimorph_repos.txt > validated_codes.txt

while read -r code; do
    output_dir="unimorph/data/${code}"
    output_file="${code}.tab"

    if [[ -f "$output_dir/$output_file" ]]; then
        echo "Skipping ${code} - file already exists: ${output_file}"
        continue
    fi

    mkdir -p ${output_dir}
    curl -L -o "${output_dir}/${output_file}" "https://raw.githubusercontent.com/unimorph/${code}/refs/heads/master/${code}"
    echo "Downloaded ${code} dataset"
    sleep 5
done < validated_codes.txt
