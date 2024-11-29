import os
import json


from openai import OpenAI
from pydantic import BaseModel

from config.config import config



class Title(BaseModel):
    event_title: str

def get_title(client=OpenAI(),event="") -> str:

    if "" == event:
        raise ValueError
    
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Your task is to find a small descriptive title for the provided event. here an example <Event>The conflict rages on as the beholder re-enters the battlefield, its ominous presence looming over the combatants.</event><title>Battle Continuation</title>"
   
            },
            {
                'role': 'user',
                'content': event
            },
        ],
        
        response_format=Title
    )
    title_obj = json.loads(response.choices[0].message.content)
    
    print(title_obj["event_title"])

    return title_obj["event_title"]

def event_title(session_id):
    

    journal_path = os.path.join(config.DATA_FOLDER, session_id, "journal.json")
    save_path = os.path.join(config.DATA_FOLDER, session_id, "title_journal.json")

    try:
        with open(journal_path, "r") as jrnl:
            journal = json.load(jrnl)
    except FileNotFoundError:
        raise FileNotFoundError

    for location in journal["chronology_of_events"]:
        for event in location["events"]:

            response = get_title(event=event["description"])

            event["event_title"] = response


    with open(save_path, "w") as titlejrnl:

        json.dump(journal, titlejrnl, indent=4)

    
    return journal

if __name__ == "__main__":
    client=OpenAI()
    session_id = "20240909"
    event_title(session_id)        
        