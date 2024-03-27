from pydub import AudioSegment
import os 
import simpleaudio as sa
from gradio_client import Client,file

app_url="https://00b2e7df15100f5e4c.gradio.live/" 
#make sure app_url ends with a slash

#The Model LLaMA2-13B-Psyfighter2-GPTQ supports 18+ content.
# Please make sure you wrote the correct RolePlay and Response.
# Otherwise, the model give you 18+ response that may embarrass you in public.

RolePlay="You are my girlfriend. You are supportive and understanding."
Response="Hey love, I'm here for you. What's on your mind? Talk to me."

try:
    client = Client(app_url)
except:
    print("Error: Could not connect to the server. Please make sure the URL is correct and the server is running.")

def mp3_to_wav(mp3_file, wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")


if not os.path.exists("./audio"):
    os.makedirs("./audio")


def play_audio(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()



def describe_image(RolePlay, Response,prompt):
    if len(prompt) == 0:
        prompt ="Hi, How are you?"
    result = client.predict(
        RolePlay, 
        Response,
        prompt,	
        api_name="/predict"
        )
    # print(result)
    mp3_file = result
    base_path = os.path.basename(mp3_file).split(".")[0]
    wav_file = f"./audio/{base_path}.wav"
    mp3_to_wav(mp3_file, wav_file)
    play_audio(wav_file) 
    os.remove(mp3_file) 
    os.remove(wav_file)  
from whisper_mic import WhisperMic

mic = WhisperMic(model="tiny.en")
def speech_recognition():
    while True:  
        try:
            play_audio("okay.wav")
            text = mic.listen()
            print("You said:", text)
            
            # pronunciations = ["alisha", "alisa", "alyssa"]  # Add any variations you want to consider

            # matching_variation = next((variation for variation in pronunciations if variation in text.lower()), None)

            # if matching_variation:
            #     print(f"Matched variation: {matching_variation}")
            #     print("Triggering the API...")
            #     play_audio("okay.wav")
            #     prompt = text.lower().split(matching_variation)[-1].strip()
            #     prompt = prompt.strip().replace(",", " ").strip()
            #     print("Prompt:", prompt)
            #     describe_image(RolePlay, Response,prompt)
            # else:
            #     print("No matching variation found.")
            if text:
                prompt=text
                describe_image(RolePlay, Response,prompt)    
            else:
                print("No text detected.")    
        except Exception as e:
            print(e)

speech_recognition()
 
