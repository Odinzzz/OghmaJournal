import json
import os

from config.config import config
import decorator

@decorator.timer
def add_envent_to_journal() -> None:

    session_id = input("session id: ")

    event_path = os.path.join(config.DATA_FOLDER, session_id, "events.json")

    with open(event_path, "r") as event_file:
        events = json.load(event_file)

    formated_events = []

    for event in events:

        formated_event= {
                    "step_number": "",
                    "event_title": "",
                    "description": event
                }
        
        formated_events.append(formated_event)

    
    journal_path = os.path.join(config.DATA_FOLDER, session_id, "journal.json")

    with open(journal_path, "r", encoding="utf-8" ) as journal_file:
        journal = json.load(journal_file)

    journal["chronology_of_events"][0]["events"]= formated_events

    with open(journal_path, "w", encoding="utf-8" ) as journal_file:
        json.dump(journal, journal_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    add_envent_to_journal()