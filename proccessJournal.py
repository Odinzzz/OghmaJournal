import os
import json

from scripts.toDiscord import to_discord
from scripts.tag import tagging
from scripts.event_title import event_title
from scripts.summary import summary
from scripts.toHtml import toHtml
from scripts.merge_tag import merge_tag
from config.config import config

Debug = True
while True:
    
    session_id = input("Session ID: ")

    session_journal_path = os.path.join(config.DATA_FOLDER, session_id, "journal.json")
    session_html_path = os.path.join(config.DATA_FOLDER, session_id, "journal.html")
    # Load the journal file
    try:
        journal = event_title(session_id)
        break
    except FileNotFoundError:
        print(f"No session id: {session_id} found")


used_tags = []



# Process each event in the chronology of events
for location in journal["chronology_of_events"]:
    # Fixing the print statement to use single or escaped quotes inside f-string
    print(f"processing event at {location['location']}")

    for event in location["events"]:
        # Call the tagging function for each event description
        tag_job = tagging(event["description"], debug=Debug)

        # Store the tagged string back in the event
        event["tagged_description"] = tag_job["tagged_string"]

        # Append all used tags from the tagging process
        for tag in tag_job["use_tags"]:
            used_tags.append(tag)

# Dump the updated journal back to a file
with open(os.path.join(config.DATA_FOLDER, session_id,"journaldump.json"), "w", encoding="utf-8") as journaldump:
    json.dump(journal, journaldump, indent=4)

# remove duplicate and Dump the used tags to a separate file 


with open(os.path.join(config.DATA_FOLDER, session_id,"useTagdump.json"), "w", encoding="utf-8") as tagdump:
    json.dump(merge_tag(used_tags), tagdump, indent=4)

journal = summary(journal,session_id)

to_discord(journal,session_id)


html_journal = toHtml(journal)

with open(session_html_path, "w") as file:
    file.write(html_journal)
    

