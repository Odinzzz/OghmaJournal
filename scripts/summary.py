import json
import os

from pydantic import BaseModel
from openai import OpenAI

from config.config import config



class event(BaseModel):
    event_title: str
    impact: str

class conclusion(BaseModel):
    summary: str
    key_events: list[event]

def summary(journal, session_id):


    summary = ""

    for location in journal["chronology_of_events"]:
        summary += f"Location: {location['location']}\n"
        for entry in location['events']:
            summary += f"event title: {entry['event_title']}\n{entry['description']}"


    client = OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": 'Summarize this DnD story in a short text as if the narrator was part of the adventure, explaining what happened during the adventure, and record a maximum of three key events.'},
            {"role": "user", "content": summary}
        ],
        response_format=conclusion
    )

    summary = json.loads(response.choices[0].message.content)

    journal['conclusion'] = summary


    with open(os.path.join(config.DATA_FOLDER, session_id,"journalFinal.json"), "w") as final:

        json.dump(journal,final,indent=4)

    return journal



if __name__ == "__main__":

    
    try:
        with open("journaldump.json", "r") as journal:

            json_journal = json.load(journal)
    except:
        print("ERROR")