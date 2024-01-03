from ObjectChar import *
# Voice/Narration; Note: Need to install ffmpeg
from elevenlabs import set_api_key
from elevenlabs import voices
import random

# Set API Keys
set_api_key("cbf347afc06326009118b58a7332ee59")

# Save the voices available to use via the ElevenLabs API
voices = voices() 
maleVoices = []
femaleVoices = []
# Sort voices into male and female voices
for voice in voices:
    if (voice.labels['gender'] == 'male'):
        maleVoices.append(voice)
    else:
        femaleVoices.append(voice)

def selectVoice(charGender):
    '''Randomly return a gender-specific voice out of available voices'''
    if (charGender == "Man"):
        randomIndex = random.randint(0,len(maleVoices)-1)
        selectedVoice = maleVoices[randomIndex]
        maleVoices.remove(maleVoices[randomIndex])
        return selectedVoice
    else:
        randomIndex = random.randint(0,len(femaleVoices)-1)
        selectedVoice = femaleVoices[randomIndex]
        femaleVoices.remove(femaleVoices[randomIndex])
        return selectedVoice
    
def setCharacter(character):
    '''Create ObjectChar objects to store the gpt-generated characters'''
    finalCharacter = ObjectChar("n/a", "n/a", "n/a", "n/a", "n/a", "n/a",) # An empty character to-be-filled
    charAttributes = character.split("\n")

    for attribute in charAttributes:
        attribute = attribute.strip(" ")
        attributeCategory = attribute.partition(":")[0]
        attributeValue = attribute.partition(":")[2].strip()

        # Rename the gpt-generated categories to names that match ObjectChar class variables
        if (attributeCategory == "Name"):
            attributeCategory = "name"
        elif (attributeCategory == "Age Group"):
            attributeCategory = "ageGroup"
        elif (attributeCategory == "Gender"):
            attributeCategory = "gender"
        elif (attributeCategory == "Personality"):
            attributeCategory = "personality"
        elif (attributeCategory == "Appearance"):
            attributeCategory = "appearance"

        setattr(finalCharacter,attributeCategory,attributeValue)

    return finalCharacter  

def assignCharVoice(character):
    '''Assign a voice to an input character'''
    charGender = character.gender # Man or Woman
    character.voice = selectVoice(charGender)



''' Helpful reminders with AI-voice API'''
    #testVoice = selectVoice("Male")
    #testObject = ObjectChar("TestObject","Male","Middle-Aged","Calm","Professional",testVoice)

'''
    testAudio = generate(
        text = f"Hi! My name is {testObject.name}", # will need to swap out the name for the name of the obect
        voice = testObject.voice.name
        )
    play(testAudio)
'''