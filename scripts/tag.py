import os
import json

from pydantic import BaseModel
from openai import OpenAI
from typing import List

from config.config import config


class tag(BaseModel):
    name: str
    tag: str

class tagDict(BaseModel):    
    Characters: List[tag]
    Places: List[tag]
    

class TagJob(BaseModel):
    task: str
    tagged_string: str
    use_tags: List[tagDict]

    

def add_tag(client=OpenAI(), content=' ' ):
    '''
        ask open ai to add FoundryTag from a tag list

    '''
    # TODO: change the file path to os.
    all_tag_path = os.path.join("reference","alltag.json")
    with open(all_tag_path, "r", encoding="utf-8") as alltag:

        tags = str(json.load(alltag))

    # prompt = "Your work is of analyzing the input of the user and of replacing the word that have need of being by the tag in this Json:" 
    # prompt = "Your work is to analyze the input of the user and to replace the words that need to be tagged with those:"
    prompt = "task: tagging. Your work is to analyze the input of the user and replace the words that need to be tagged with those:"

    prompt += tags

    prompt += "When a notable name or place not already in the list is identified, create a new tag. log all the tag use in use_tags"

                

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                'role': 'user',
                'content': content
            },
        ],
        
        response_format=TagJob
    )

  
    return response.choices[0].message.content


def tagging(content, debug=False):
    '''
    -> str

    Adds Foundry VTT JournalEntryTag

    tagJob -> 
    '''


    results = []

    # Generate 5 response for exactitude
    for i in range(5):

        response = add_tag(content=content) 

        responseJson = json.loads(response)
        responseJson["id"] = i
        results.append(responseJson)

        # log file for debug
        # if debug:
        #     file_name = f'test{i}.json'
        #     file_path = os.path.join(config.DEBUG_FOLDER, 'json_files', file_name)
        #     with open(file_path, "w", encoding="utf-8") as file:
        #         json.dump(responseJson, file, indent=4)


    # base score on similarity
    for check in results:        
        check["score"] = 0
        for result in results:
            if check["tagged_string"] == result["tagged_string"]:
                check["score"] += 1
            if len(check["use_tags"]) == len(result["use_tags"]):
                check["score"] += 1
            try:
                
                if len(check["use_tags"][0]["Characters"]) == len(result["use_tags"][0]["Characters"]):
                    check["score"] += 1
            except KeyError as e:
                print(e)
            except IndexError as e:
                print(e)    
            try:
                
                if len(check["use_tags"][0]["Places"]) == len(result["use_tags"][0]["Places"]):
                    check["score"] += 1
            except KeyError as e:
                print(e)
            except IndexError as e:
                print(e)                 

    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)

    if debug:
        for sorted_result in sorted_results:
            print(f"ID: {sorted_result['id']} score: {sorted_result['score']}")

        try:
            print(f"Chosen ID: {sorted_results[0]["id"]}")
        except:
            print("Chosen ID: None")

        print(f"{sorted_results[0]["tagged_string"]}")

    return sorted_results[0]                


if __name__ == "__main__":
    content = "Despite launching a powerful crossbow assault, the knights are bewitched by the harpies' enthralling song, rendering them helpless. The harpies then unleash a barrage of magical missiles at Ssurruk, resulting in his tragic explosion from the impact."
    
    tagging(content, debug=True)


