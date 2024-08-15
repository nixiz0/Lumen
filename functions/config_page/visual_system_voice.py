import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import threading
import numpy as np
import math
import wave
import simpleaudio as sa


class VisualSyntheticVoice:
    def __init__(self):
        self.screen_width = 260
        self.screen_height = 260
        self.CHUNK = 380 # More high value of CHUNK => More quickly are sinusoid
        pygame.init()
        pygame.display.set_caption("Synthetic Voice")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

    def draw_sine_wave(self, amplitude):
        self.screen.fill((0,0,0))
        points = []
        if amplitude > 10:
            for x in range(self.screen_width):
                y = self.screen_height/2 + int(amplitude * math.sin(x * 0.05))
                points.append((x,y))
        else: 
            points.append((0, self.screen_height/2))
            points.append((self.screen_width, self.screen_height/2))
        pygame.draw.lines(self.screen, (0, 189, 255), False, points, 2) # Cyan color lines
        pygame.display.flip()

    def play_audio(self, filename="functions/config_page/temp_output_voice/voice_output.wav"):
        # Load .wav file
        wave_obj = sa.WaveObject.from_wave_file(filename)

        # Define a function to play the audio
        def play_audio_thread():
            # Play .wav file
            play_obj = wave_obj.play()

            # Wait for the .wav file to end
            play_obj.wait_done()

        # Start a new thread to play the audio
        audio_thread = threading.Thread(target=play_audio_thread)
        audio_thread.start()

        # Playing the .wav file
        wav_file = wave.open(filename, 'rb')

        running = True 
        while running:
            data = wav_file.readframes(self.CHUNK)
            if data:
                data_np = np.abs(np.frombuffer(data, dtype=np.int16))
                data_np = np.square(data_np)
                if np.isnan(data_np).any() or np.isinf(data_np).any():
                    data_np = np.nan_to_num(data_np)  # replace NaN or inf values with zero
                mean_val = np.mean(data_np)
                rms = np.sqrt(mean_val + 1e-10) if mean_val >= 0 else 0  # add a small constant for numerical stability
                self.draw_sine_wave(rms)
            else:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clock.tick(60)
        wav_file.close()