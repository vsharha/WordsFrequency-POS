from process_datasets.combine_datasets.combine_datasets import output_combined, output_combined_single

if __name__ == "__main__":
    # output_combined()
    
    # print("\nCombining NOUNS...\n")
    # output_combined(output_dir="datasets/nouns", parts_of_speech=["N"], output_pos_tags=False, inflections=False, check_inflections=True)
    # print("\nCombining VERBS...\n")
    # output_combined(output_dir="datasets/verbs", parts_of_speech=["V"], output_pos_tags=False, inflections=False, check_inflections=True)
    # print("\nCombining ADJECTIVES...\n")
    # output_combined(output_dir="datasets/adjectives", parts_of_speech=["ADJ"], output_pos_tags=False, inflections=False, check_inflections=True)

    output_combined(output_dir="datasets/wordle++/", parts_of_speech=[["N"], ["V"], ["ADJ"]], output_pos_tags=False, inflections=False, check_inflections=True, regex=r'^[^\-\/\+\=\*\&\%\$\#\@\!\?\.\,\;\:\(\)\[\]\{\}\|\\\"\'\`\~\^\<\>\d\s]{2,8}$')
    
    # TODO: Combine frequency data for multiple inflections