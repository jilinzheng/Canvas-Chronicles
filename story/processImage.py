import os
from openai import OpenAI
from PIL import Image
import base64
import json
import requests

client = OpenAI(api_key = "YOUR KEY HERE")          #openai key

asticaAPI_key = '60CE9B85-35A6-4D39-80BF-9B1C5B42A21964A2F626-05FF-427C-B9CE-ACB564E0AE59'  # visit https://astica.ai      #astica key
asticaAPI_timeout = 50 # in seconds. "gpt" or "gpt_detailed" require increased timeouts
asticaAPI_endpoint = 'https://vision.astica.ai/describe'
asticaAPI_modelVersion = '2.1_full' # '1.0_full', '2.0_full', or '2.1_full'

asticaAPI_visionParams = 'gpt,describe,objects,faces'  # comma separated, defaults to "all". 
asticaAPI_gpt_prompt = '' # only used if visionParams includes "gpt" or "gpt_detailed"
asticaAPI_prompt_length = '90' # number of words in GPT response

asticaAPI_input = input("Enter an image http link to get started: ")
    #'https://astica.ai/example/asticaVision_sample.jpg'

def asticaAPI(endpoint, payload, timeout):
    response = requests.post(endpoint, data=json.dumps(payload), timeout=timeout, headers={ 'Content-Type': 'application/json', })
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'error': 'Failed to connect to the API.'}

def chatWithChat(query):
   response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
   response_text = response.choices[0].message.content
   return response_text
   
# Originally main
def processImage():
    # Define payload dictionary
    asticaAPI_payload = {
        'tkn': asticaAPI_key,
        'modelVersion': asticaAPI_modelVersion,
        'visionParams': asticaAPI_visionParams,
        'input': asticaAPI_input,
    }
    # call API function and store result
    asticaAPI_result = asticaAPI(asticaAPI_endpoint, asticaAPI_payload, asticaAPI_timeout)

    query = """Give me random name(s) (first and last), age group(s) (child, teen, adult, or senior), gender(s) (man/woman), 
            object name(s) (e.g. balloon, water bottle), personality attributes (e.g. charismatic, pessimistic), 
            and appearance(s) for each of the following inanimate objects while also not changing them to humans.
            Ensure your output format is NOT numbered AND in the following SAMPLE format BUT DO NOT INCLUDE THE SAMPLE below:
            
            Characters: {
                Name: Sample Character
                Age Group: Adult
                Gender: Man
                Object: Banana
                Personality: Cheerful, optimistic
                Appearance: Bright yellow with a friendly smile
    
            }
            
            Beginning Prompt:
                [Some Prompt]
            """
    for i in range(len(asticaAPI_result['objects'])):
        query = query + asticaAPI_result['objects'][i]['name'] + " "
    query = query + ". Use the following caption to help decide their personality. "
    query = query + asticaAPI_result['caption']['text']
    query = query + " Then, formulate a beginning prompt for a story speaking from the narrator's perspective using the objects as characters. "
    response_text = chatWithChat(query)       # query is what you are asking chatgpt
    print("Your image has been processed as:")
    print(asticaAPI_result['caption']['text'])
    return response_text

if __name__ == "__main__":
    processImage()
