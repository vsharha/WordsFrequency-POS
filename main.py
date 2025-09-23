from process_datasets.fetch_datasets import unimorph
from process_datasets.fetch_datasets import frequency

if __name__ == "__main__":
    unimorph_codes: list[str] = unimorph.fetch_codes()
    frequency_codes: list[str] = frequency.fetch_mapped_codes()

    codes_intersection: list[str] = list(set(unimorph_codes).intersection(set(frequency_codes)))

    frequency.download_datasets(list(codes_intersection))
    unimorph.download_datasets(list(codes_intersection))