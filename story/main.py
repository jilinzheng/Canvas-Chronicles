import re
import time

# Scripts
from processImage import *  # Jared: process image and get the objects
from getStory import *      # Mete: create AI-generated story involving objects
from getVoices import *     # Jilin: assign AI-generated voice to objects
from ObjectChar import *    # Objects' class

finalizedChars = []         # An array to store the characters into the ObjectChar class

def main():
    '''Take the user-inputted image and generate characters as well as a beginning context'''
    #print("entered finalizeCharacters in main.py")
    charsAndContext = processImage()
    # sampleOutput = main()
    
    charsAndContext = charsAndContext.strip()
    # Partition the output for just the characters
    partitionedOutput = charsAndContext.partition("Beginning Prompt")
    characters = partitionedOutput[0]
    plot = partitionedOutput[2]

    # List of individual characters
    objectChars = partitionedOutput[0].split("\n\n") # Might have an extra useless entry
    objectChars = objectChars[0:len(objectChars)-1]

    # Loop through the first partition (the identified objects)
    characterCount = 0
    for character in objectChars:
        # Create and save ObjectChar objects with the current character
        finalizedChars.append(setCharacter(character))
        finalizedChars[characterCount].voice = assignCharVoice(finalizedChars[characterCount])
        characterCount+=1

    # Print the current character's attributes and have the character introduce themselves
    for character in finalizedChars:
        assignCharVoice(character)
        #Uncomment when voice is wanted
        testAudio = generate(
            text = f"Hi! My name is {character.name}. It is a pleasure to meet you!",
            voice = character.voice.name
        )
        print(f"Hi! My name is {character.name}. It is a pleasure to meet you!")
        play(testAudio)

    generateStory(finalizedChars,plot)
        
if __name__ == "__main__":
    start = time.time()

    main()

    end = time.time()
    print(end - start,"seconds elapsed.")