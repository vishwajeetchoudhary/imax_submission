from google.cloud import speech,texttospeech
import speech_recognition as sr
from config.settings import DEFAULT_LANGUAGE_CODE,AUDIO_OUTPUT_PATH,DEFAULT_SPEECH_GENDER

class SpeechService:
    def __init__(self):
        try:
            self.speech_client = speech.SpeechClient()
            self.tts_client = texttospeech.TextToSpeechClient()
            print("Speech service initialized successfully")
        except Exception as e:
            print(f"Error initializing speech service: {e}")
            raise
    
    def recognize_speech_from_mic(self,language_code=DEFAULT_LANGUAGE_CODE):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Please Speak now")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio,language=language_code)
            print(f"Recognized Speech: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError:
            print("speech recognition service unavailable")
            return None
        except Exception as e:
            print(f"Error occured: {e}")
            return None
        
    def recognize_speech_from_file(self,audio_path,language_code=DEFAULT_LANGUAGE_CODE):
        try:
            with open(audio_path,"rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content = content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                sample_rate_hertz=16000,
                language_code=language_code
            )
            response = self.speech_client.recognize(config=config,audio=audio)
            return response.results[0].alternatives[0].transcript if response.results else ""
        except Exception as e:
            print(f"Error recognizing speech from file: {e}")
            return ""
    
    def synthesize_speech(self,text, output_path=AUDIO_OUTPUT_PATH,language_code=DEFAULT_LANGUAGE_CODE):
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=DEFAULT_SPEECH_GENDER
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding = texttospeech.AudioEncoding.MP3,
                speaking_rate=1.1
            )
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,voice=voice,audio_config=audio_config
            )
            with open(output_path,"wb") as out:
                out.write(response.audio_content)
            
            print(f"Speech synthesized and saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"Error synthesizing speech : {e}")
            return None