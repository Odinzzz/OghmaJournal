import json
import os
from datetime import datetime

from config.config import config
import decorator

@decorator.timer
def make_file() -> None:
    # Get the current date in yyyymmdd format
    current_date = datetime.now().strftime("%Y%m%d")


    # Create a directory with the current date
    os.makedirs(os.path.join(config.DATA_FOLDER, current_date), exist_ok=True)

    # Define the path for the journal.txt file
    journal_path = os.path.join(config.DATA_FOLDER, current_date, "journal.json")

    #load template
    template_path = os.path.join(config.REFERENCE_FOLDER, "journal_template.json")
    try:
        with open(template_path, "r") as file:
            journal_template = json.load(file)
    except FileNotFoundError as e:
        print(f"Template fail to load in memory: {e}")

    journal_template["session_id"] = current_date
    # Create the journal.txt file
    with open(journal_path, "w") as journal_file:
        json.dump(journal_template, journal_file, indent=4)

    print(f"Directory '{current_date}' created with 'journal.json' inside it.")
    
if __name__ == "__main__":
    make_file()