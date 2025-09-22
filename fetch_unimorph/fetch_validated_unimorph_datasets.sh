#!/usr/bin/env bash
set -euxo pipefail

python iso_639/check_iso_code.py --codes_file fetch_unimorph/unimorph_repos.txt > fetch_unimorph/validated_codes.txt

# while read -r code; do
#     output_dir="datasets/unimorph/${code}"
#     output_file="${code}"

#     if [[ -f "$output_dir/$output_file" ]]; then
#         echo "Skipping ${code} - file already exists: ${output_file}"
#         continue
#     fi

#     mkdir -p ${output_dir}

#     response=$(curl -s -L "https://raw.githubusercontent.com/unimorph/${code}/refs/heads/master/${code}")
#     if [[ "$response" == "404: Not Found" ]]; then
#         echo "404 Error on branch master, trying branch main..."

#         response=$(curl -s -L "https://raw.githubusercontent.com/unimorph/${code}/refs/heads/main/${code}")

#         if [[ "$response" == "404: Not Found" ]]; then
#             echo "Couldn't download dataset ${code}"
#             continue
#         fi
#     fi

#     echo "$response" > "${output_dir}/${output_file}"
#     echo "Downloaded ${code} dataset"
    
#     sleep 5
# done < fetch_unimorph/validated_codes.txt
