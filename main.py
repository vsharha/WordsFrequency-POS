from process_datasets.combine_datasets.combine_datasets import output_combined

if __name__ == "__main__":
    output_combined()
    
    output_combined(output_dir="datasets/nouns", parts_of_speech=["N", "SG"], output_pos_tags=False, inflections=False)
    output_combined(output_dir="datasets/verbs", parts_of_speech=["V", "SG"], output_pos_tags=False, inflections=False)