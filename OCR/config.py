folders_to_watch = [
    'c:\\temp\\'
    # Add more folders to watch as needed separated by commas
]

folder_solr_mapping = {
    "c:\\temp\\": {
        "solrUrl": "http://localhost:8983/solr/Aquarius",
        "path_replacement_pairs": [
            #("old_path_1", "new_path_1")
            #("old_path_2", "new_path_2"),
            # Add more replacement pairs as needed
        ]
    },
    # Add more folder_solr_mapping entries as needed
}

process_existing_text_files = False
process_existing_image_files = False