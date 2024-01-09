# Canvas Chronicles
## Summary
Canvas Chronicles is an application that allows users to create their own children stories with a simple picture. With our application, users simply can upload a picture of their choice. After that, the future of the story is in the hands of the AI! First our application processes the image and find the objects in the image. Then, it gives each object a personality, a **voice**, and creates a story based on the objects!

This project originated out of BostonHacks 2023!

## Running the App
You will need to have an account created with the following AI technologies for their respective APIs: [OpenAI](https://openai.com/blog/openai-api), [asticaVision](https://astica.ai/vision/documentation/), [ElevenLabs](https://elevenlabs.io/docs/api-reference/text-to-speech).

For ElevenLab's voice AI, you will also need to have [ffmpeg](https://ffmpeg.org/download.html) installed.

Simply generate API keys for each service, clone this repo, and paste your keys into where it says `YOUR KEY HERE` in the `processImage.py`, `getStory.py`, and `getVoices.py` Python scripts.

Finally, run the `main.py` script to execute the application! Have fun writing your story!

## [Demo Video](https://youtu.be/ofC4NujWLWE){:target="_blank"}

## Known Issues
- ChatGPT sometimes generates new characters, which are unaccounted for and thus break the script
- ChatGPT's response are occasionally too long, which may conflict with ElevenLabs' API quotas

## Project Inspiration
After reading about the Digital Dreamers track (as part of BostonHacks 2023), we began to reminisce about the good old days of reading childrens books. We missed the adventure, suspense, and creativity that came with reading childrens books. We set out to bring back that feeling of adventure and creativity with our application. We wanted to create a platform where users could take simple pictures with generatic object and turn them into magnificent stories.

We hope you love our application as much as we do! If you have any suggestions, please feel free to reach out to us!

## Project Contributors
Mete Gumusayak, Noah Robitshek, Jared Solis, Jilin Zheng
