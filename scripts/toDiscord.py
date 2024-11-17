import json
import os

from openai import OpenAI
from pydantic import BaseModel

from config.config import config




class Translation(BaseModel):
    text: str

class Summary(BaseModel):
    summary: str

def dnd_it(client=OpenAI(),prompt=""):

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages = [
            {
                "role": "system",
                "content": "Your role is to  make a one paragraph summary of the event."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=Summary
    )

    return completion.choices[0].message.content


def translate(client=OpenAI(),prompt=""):
        
    completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages = [
        {
            "role": "system",
            "content": "Your role is to take the user input and translate it in french for ¸"
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    response_format=Translation
    )

    return completion.choices[0].message.content


def to_discord(journal,session_id):

    resume = json.dumps(journal["chronology_of_events"], indent=4)
    # for location in journal["chronology_of_events"]:

    #     # resume += f"Event at {location['location']}:\n"

    #     for event in location["events"]:
    #         resume += f" {event["event_title"]}:"
    #         resume += f" {event['description']}"

    print(resume)
    discord = json.loads(dnd_it(prompt=resume))

    traduction = json.loads(translate(prompt=discord["summary"]))


    dump_path = os.path.join(config.DATA_FOLDER, session_id, "discord.json")


    with open(dump_path, "w", encoding='utf-8') as dmp:
        json.dump([discord,traduction], dmp, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    session_id = input("session id: ")
    journal_name = input("journal name: ")
    journal_path = os.path.join(session_id, journal_name)

    
    with open(journal_path, "r") as jrnl:

        journal = json.load(jrnl)
    
    to_discord(journal,session_id)

