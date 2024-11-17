import json
from openai import OpenAI 
from pydantic import BaseModel
from typing import Dict, List


class LocationEvents(BaseModel):
    location: str
    events: List[str]
class DnDEventSummary(BaseModel):
    # Define a dictionary with dynamic keys (character names) and list of strings (events)
    summary: List[LocationEvents]



client = OpenAI()

content: str = "<ol><li>Dynnegal:<ol><li>The day begins with Ssurruk casting True Resurrection on Kezilok, restoring him to life, free from any charm and ready to rejoin the battle.</li><li>Attempting to escape the chaos below, Rol flies high into the air, but his shield is dispelled by kobold wizards. Seizing the opportunity, the harpies unleash a volley of magic missiles that strike Rol down, causing his lifeless body to plummet to the ground like a stone.</li><li>Elfwynn manages to dispel the beholder&#39;s protective enchantments, forcing the beholder to make a tactical retreat behind enemy lines.</li></ol></li><li>Moray:<ol><li>The conflict rages on as the beholder re-enters the battlefield, its ominous presence looming over the combatants.</li><li>Suddenly, the sky darkens, filled with blood-red, menacing clouds that cast eerie crimson pools upon the battlefield, heightening the sense of dread.</li></ol></li></ol>"

def quill_processing(client=OpenAI(),content="" ) -> DnDEventSummary:
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "I have an example of HTML structure that outlines a Dungeons & Dragons (DnD) session, shown as nested ordered lists. The structure represents locations and events that occurred in each location. The task is to transform this HTML structure into a JSON object. The JSON object should be formatted such that each location acts as a key, and the corresponding value is a list of events that occurred in that location. \n\nHere is an example of the HTML structure: \n\n```html\n<ol>\n    <li>Dynnegal:\n        <ol>\n            <li>we fought someone</li>\n            <li>we loot a cavern</li>\n            <li>we sleep in an inn</li>\n        </ol>\n    </li>\n    <li>Moray:\n        <ol>\n            <li>we did something</li>\n            <li>we buy some items</li>\n        </ol>\n    </li>\n</ol>\n```\n\nPlease transform this HTML example into a JSON object with the format:\n\n```json\n{\n  \n  \"Dynnegal\": [\"we fought someone\", \"we loot a cavern\", \"we sleep in an inn\"],\n    \"Moray\": [\"we did something\", \"we buy some items\"]\n}\n```"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": content
            }
        ]
        },
        
    ],
    
    response_format=DnDEventSummary
    )

    

    obj = response.choices[0].message.parsed
    objs = response.choices[0].message.content

    print(obj.summary[0].location)

    for locations in obj.summary:
        print(locations.location)
        for event in locations.events:
            print("    ", event)
    

if __name__ == "__main__":
    quill_processing(content=content)  