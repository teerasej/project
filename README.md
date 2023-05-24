
# Extract intent from the voice file - MS Reactor

I create this project for demonstrate how to leverage Azure OpenAI Service with other Azure Cognitive service to provide intelligent solution.

## Setup 

You should create your `.env` file with following variables: 

```
AZURE_SUBSCRIPTION_KEY=
AZURE_REGION=

OPENAI_ENDPOINT=
OPENAI_API_KEY=
```

## Noted

- Please use `.wav` file, `.m4a` file will cause the error in following line: 

```python
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
```