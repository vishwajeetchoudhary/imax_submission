import os
import platform
import subprocess
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from pygame import mixer

class AudioService:  
    def __init__(self):
        self.initialized = False
    
    def play_audio(self, file_path):
        try:
            if platform.system() == "Windows":
                if not self.initialized:
                    mixer.init()
                    self.initialized = True
                    
                mixer.music.load(file_path)
                mixer.music.play()
                while mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                mixer.music.unload()
            elif platform.system() == "Darwin":
                subprocess.call(["afplay", file_path])
            else:
                if os.system("which mpg123 > /dev/null") == 0:
                    subprocess.call(["mpg123", file_path])
                elif os.system("which mpg321 > /dev/null") == 0:
                    subprocess.call(["mpg321", file_path])
                else:
                    if not self.initialized:
                        mixer.init()
                        self.initialized = True
                        
                    mixer.music.load(file_path)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    mixer.music.unload()
            return True
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False