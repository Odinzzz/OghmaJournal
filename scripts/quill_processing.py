from typing import List, Dict
from bs4 import BeautifulSoup


def quill_processing(html: str, list_type: str = 'ol') -> List[Dict[str, List[str]]]:
    """
    Processes an HTML string containing ordered or unordered lists with nested list items.
    Extracts the top-level list items and their nested items into a list of dictionaries.

    Args:
        html (str): A string containing HTML with one or more ordered (`<ol>`) or unordered (`<ul>`) lists 
                    and nested list items (`<li>`).
        list_type (str): The type of the list to process ('ol' for ordered list or 'ul' for unordered list).
                         Defaults to 'ol'.

    Returns:
        List[Dict[str, List[str]]]: A list of dictionaries where each dictionary contains a top-level list item
                                     as the key, and its corresponding nested list items as a list of strings.

    Raises:
        ValueError: If no `<ol>` or `<ul>` list is found in the HTML, depending on the `list_type` argument.
    """
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find the top-level list based on the list_type argument ('ol' or 'ul')
    list_tag = soup.find(list_type)
    if not list_tag:
        raise ValueError(f"No {list_type} found in the HTML.")

    # Extract all top-level list items, excluding nested lists
    top_level_items = list_tag.find_all('li', recursive=False)

    lists = []
    for item in top_level_items:
        # Extract the name of the top-level item (text content of <li>)
        name = item.contents[0].strip()
        
        # Find all nested <li> elements within this top-level <li>
        nested_items = item.find_all('li')
        
        # Extract the text content of each nested <li>
        list_of_nested = [nested_item.text for nested_item in nested_items]
        
        # Append the dictionary with top-level item and its nested items
        lists.append({name: list_of_nested})

    return lists 

# [
#     {
#         "Dynnegal": [
#             "Buy",
#             "sell",
#             "fight talk"
#         ]
#     },
#     {
#         "moray": [
#             "eat",
#             "sleep",
#             "swim"
#         ]
#     }
# ]
