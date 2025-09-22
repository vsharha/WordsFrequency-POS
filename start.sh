#!/usr/bin/env bash
set -euxo pipefail

# TODO: add fetching of FrequencyWords

bash fetch_unimorph/fetch_all_codes.sh
bash fetch_unimorph/fetch_validated_unimorph_datasets.sh