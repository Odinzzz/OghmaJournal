import json
from openai import  OpenAI
from pydantic import BaseModel

class SearchResponse(BaseModel):
    exist: bool
    name: str
    foundry_tag: str

class Correction(BaseModel):
    success: bool
    original: str
    french: str
    english: str





def ai_check(string, object, client=OpenAI()) -> dict:
    """
    docstring
    """

    object_string = json.dumps(object)
    exemple_string = json.dumps({'exist': False, 'name': "Baldur's Gate", 'foundry_tag': '@JournalEntry[Baldur\'s Gate]{Baldur\'s Gate}'})
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Check if the user prompt is in this object: {object_string}. Sometimes, the user makes typos. If you are sure that the user means something else, correct the word. If it does not exist, create a tag. For example, input: 'baldur Gate', output: {exemple_string}. Explanation: The name are Case sensitive. In the foundry tag, the word inside [] is the foundry name of the journal, and the {{}} is the string displayed."
            },
            {
                'role': 'user',
                'content': string
            },
        ],
        
        response_format=SearchResponse
    )

    return json.loads(response.choices[0].message.content)

def ai_corrector(string, client=OpenAI()) -> dict:
    """
    docstring
    """

    
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "I am a corrector. Provide user input in French or English, and I will correct all grammatical, lexical, and typographical errors. I can also rephrase for better structure. I will output a response like this: {original: '', french: '', english: ''}."
            },
            {
                'role': 'user',
                'content': string
            },
        ],
        
        response_format=Correction
    )

    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    
    
    string = "baldur gate"
    the_object = [{'id': 1, 'name': 'dynnegall', 'region': 'Île de Mounchi', 'tag': '@JournalEntry[Dynnegall]{Dynnegall}'}, {'id': 2, 'name': 'moray', 'region': 'Île de Mounchi', 'tag': '@JournalEntry[Moray]{Moray}'}]

    check = ai_check(string,the_object)

    print(check)