import os
import dotenv
import azure.cognitiveservices.speech as speechsdk
import openai

# Load the environment file
dotenv.load_dotenv()

# Set your Azure Cognitive Services subscription key and region
subscription_key = os.getenv('AZURE_SUBSCRIPTION_KEY')
region = os.getenv('AZURE_REGION')

# Set the path to the audio file you want to transcribe
audio_file = 'voice.wav'

# Create an audio configuration from the audio file path
audio_config = speechsdk.audio.AudioConfig(filename=audio_file)

# Create a speech configuration with your subscription key and region
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
speech_config.speech_recognition_language = "th-TH"

# Create a speech recognizer with the speech configuration
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Start recognition process asynchronously
result = speech_recognizer.recognize_once_async().get()

# Check if the recognition was successful
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    # Print the transcribed text
    print("Transcription: {}".format(result.text))

    openai.api_type = "azure"
    openai.api_base = "https://openai-nextflow.openai.azure.com/"
    openai.api_version = "2022-12-01"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        engine="MyDavinci",
        prompt=("For the below text in triple ticks, provide a JSON structure that extracts the following text into the following keys. Use provided categories for intent:\n- short_summary (in thai)\n- sentiment\n- intent: \"refund\", \"need customer support\"\n\n" 
                + "```" + result.text + "```" 
                + "\n\nResponse:}"),
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1,
        stop=None)    
    
    print(response['choices'][0]['text'])

elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))


