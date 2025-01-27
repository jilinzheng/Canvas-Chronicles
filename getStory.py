import os
from openai import OpenAI
from getVoices import *
from elevenlabs import *
from ObjectChar import *

client = OpenAI(api_key="YOUR KEY HERE")

background = """
    Limit the tokens for the response to 300 after the supplied beginning prompt.
    You are collaborativly creating an immersive play with the user.
    This story is intended to be read by children.
    Conclude each message with a request for open-ended input from the user, inviting them to actively contribute to the evolving storyline.
    Each paragraph must start with narrator if a character is not speaking.
    Ensure a seamless transition between lines, initiating each segment with the relevant character's name or the Narrator as appropriate.
    ABSOLUTELY ENSURE that each paragraph is in the following style "CHARACTER NAME: [CHARACTER DIALOGUE]."
    Maintain the integrity of the narrative by disregarding any extraneous responses that could disrupt the seamless flow of the unfolding tale.
    Should the user's input lack coherence or fail to align with the narrative possibilities, tactfully bypass the incongruity and proceed with the storyline.
    Keep the story to a minimum number of lines of dialogue and KEEP IT SHORT.
    DO NOT add actions after character names, before their dialogues, and ALWAYS use their full names.
    ALWAYS prefix lines without a character speaking, with "Narrator: ", i.e. include the narrator's name.
    DO NOT have characters speak within Narrator lines.
    DO NOT repeat names.
    Use the theme of starting an adventure, fantasy, etc.
    Do NOT introduce new characters ASIDE from those given to you with names.
    DO NOT INTRODUCE NEW CHARACTERS.
    Characters must speak ONLY dialogue; no narration.
    Limit each dialogue to 2000 characters or LESS.

    You will use the following characters in the story, and reiterate the following prompt as the beginning of the story:
    """
    # Background to tell Chat how to respond and act in the story choose 1
def startStory(history):
    '''Get initial story response from GPT.'''
    #print("Starting story.")

    response = client.chat.completions.create(                          # Get response
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": background}]+history,   # Sends background to get start of story
        max_tokens=750,                                                 # Max length of message
    )

    response_text = response.choices[0].message.content
    #print(f"The response is \n{response_text}\n")                       # Testing what response was
    return ([{"role": "assistant", "content": response_text}],response_text)

def continueStory(history):
    '''Continue story by getting additional responses from GPT.'''
    userinput = input("Enter the next event in the story below! \n")
    message = [{"role": "user", "content": userinput}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": background}] + history + message,    # Sends all messages sent in conversation to keep history
        max_tokens=300,                                                              # Max length of message
    )

    response_text = response.choices[0].message.content
    #print(f"The response is \n{response_text}\n")                                    # Testing what the response was
    #print(f"Used {response.usage.prompt_tokens} tokens with message {userinput} and {response.usage.total_tokens} in total")     # Testing to keep track of how many tokens used

    return ([{"role": "assistant", "content": response_text}] + message, response_text)

def generateStory(characters, plot):
    history = [{"role": "user", "content": plot}] # History Records all previous messages from user and chat
    text = ""
    response, text = startStory(history)        # Text is the raw response text
    readStory(characters, text)

    history = history + response                            # Initialize story
    for i in range(5):
        history = history + response  # Build history
        response, text = continueStory(history=history)     # Get response
        readStory(characters,text)
        #print(f"The history is \n {history}")               # Print history


audioFiles = []
def readStory(characters, text):
    charVoiceDict = {}
    # Store character voices in a dictionary instead of a list for faster retrieval
    for character in characters:
        charVoiceDict[character.name] = character.voice.name

    # Instantitate the narrator
    narrator = ObjectChar("Narrator","Woman","DoesItMatter?","WhyDoYouCare?","You'reAwfullyCurious","Ella - Narrator")

    ii = 0
    splitText = text.split("\n\n")                      # Split text into sections; list of sections
    for section in splitText:
        print(section,"\n")
        sectionComponents = section.partition(":")      # Partition section into names and dialogue (separated by colon)
        # Ideally GPT outputs 'Narrator:' as well so this first section is not needed
        if (sectionComponents[2] == ""):                # In the case the partition never partitions anything
            currAudio = generate(
            text = text,                                # The text is just narrator text
            voice = narrator.voice                      # So set the voice to the narrator
            )
            play(currAudio)
            continue                                    # Skip rest of loop and move to next iteration

        currCharName = sectionComponents[0]             # Current character name
        currCharDialogue = sectionComponents[2]         # Current character dialogue
        if (currCharName == "Narrator" or currCharDialogue == ""):
            currAudio = generate(                       # Audio bytes
                text = currCharDialogue,                    # The text is just narrator text
                voice = narrator.voice                      # So set the voice to the narrator
            )
            play(currAudio)
            continue
        currAudio = generate(
            text = currCharDialogue,
            voice = charVoiceDict[currCharName]         # Set the voice to the voice at the specified dictionary entry
        )
        play(currAudio)

    '''
    for line in splitText:                              # Console text output
        print(line,"\n")
    '''

if __name__ == "__main__":
    generateStory()
