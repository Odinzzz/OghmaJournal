def merge_tag(tag_dict):
    """Take a tag dump and remove the duplicate

    Args:
        tag_dict (List of tags): Tag use in the taggins proccess

    Returns:
        dict: tag without duplicate
    """
    
    seen_tags = []
    tags = {"Characters": [], "Places": []}
    

    for dump in tag_dict:

        for key in dump:

            if len(dump[key]) > 0:
                for entry in dump[key]:
                    if entry['name'] not in seen_tags:
                        seen_tags.append(entry['name'])
                        tags[key].append(entry)
    
    return tags