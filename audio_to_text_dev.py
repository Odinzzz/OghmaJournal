import json
import os
from typing import List


from openai import OpenAI
from pydantic import BaseModel

from config.config import config




class event(BaseModel):
    number: str
    description: str


class events(BaseModel):
    events: List[event]


client = OpenAI()

def main():
    session_id = input("session_id: ")
    file_name = f'{input("file name: ")}.m4a'


    audio_file = open(os.path.join(config.DATA_FOLDER, session_id, file_name), "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text",
    prompt="Bazzuc, Fremund, Dynnegale, Black onyx, Hold person"

    )
    transcript_file_path = os.path.join(config.DATA_FOLDER, session_id, "speech_to_text.txt")
    with open(transcript_file_path, "w", encoding="utf-8") as transcript_file:
        transcript_file.write(transcript)


    print(f'transcript complete go to {transcript_file_path} to review the text before procceding')
    input("press ENTER to continue.")

    with open(transcript_file_path, "r", encoding="utf-8") as transcript_file:
        transcript = transcript_file.read()

    



    response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "Separate the provided French text into distinct events, recognizing both explicit markers and implicit shifts in context when needed.\n\nConsider both clearly marked transitions and subtler cues indicating a new event. Focus on coherence and logical flow in events.\n\n# Steps\n\n1. **Identify Markers**: Look for explicit event dividers such as headers, numbers, or bullet points that indicate a new event.\n2. **Contextual Shifts**: In the absence of clear markers, identify shifts in topic, time, place, or key participants that suggest a new event has begun.\n3. **Segment Text**: Break the text into sections based on the identified markers and contextual shifts.\n4. **Review Coherence**: Ensure each segmented event is coherent and self-contained.\n\n# Output Format\n\n- Provide a list of events in a numbered format.\n- Each event should be a standalone description of what takes place, in French.\n\n# Examples\n\n**Input:**\n- \"Le matin, Jean est allé au marché. Ensuite, il a visité sa grand-mère. Le soir, il est allé au cinéma.\"\n\n**Output:**\n1. Le matin, Jean est allé au marché.\n2. Ensuite, il a visité sa grand-mère.\n3. Le soir, il est allé au cinéma.\n\n# Notes\n\n- Look for implicit shifts indicated by time phrases (e.g., \"le matin,\" \"ensuite\") and changes in action or location.\n- Ensure that the output preserves the original meaning and logical sequence of events from the text."
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": transcript
            }
        ]
        }
    ],
    temperature=1,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format=events
    )


    response_obj = response.choices[0].message.parsed

    entrys = []

    for i in response_obj.events:
        
        print(i.description)
        print()


        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Translate the given French text into English while maintaining the original meaning and context.\n\n# Steps\n\n1. Read and understand the French text provided.\n2. Identify key phrases and vocabulary that may require careful translation to maintain the text’s meaning.\n3. Translate the text into English, ensuring that nuances and context remain intact.\n\n# Output Format\n\nProvide the translated text in a clear and grammatically correct English paragraph.\n\n# Examples\n\n**Input:** \"Bonjour, comment ça va?\"\n**Output:** \"Hello, how are you?\"\n\n(Real examples should be longer and include more complex sentences and vocabulary.)"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Après que la crypte soit ouverte, les journaux changent de ton et mentionnent la déesse de la chair. Les croiseurs de fer en déduisent que les cartes et le journal mèneront à la cathédrale de la déesse de la chair."
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": "After the crypt is opened, the tone of the newspapers changes and they mention the goddess of flesh. The iron cruisers deduce that the maps and the journal will lead to the cathedral of the goddess of flesh."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": i.description
                }
            ]
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
        )
        print(response.choices[0].message.content)
        entrys.append(response.choices[0].message.content)
        print()
    
    with open(os.path.join(config.DATA_FOLDER, session_id, "events.json"), "w") as target:
        
        json.dump(entrys, target, indent=4)
if __name__ == "__main__":
    main()