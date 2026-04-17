import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder="music"):
        pygame.mixer.init()
        self.tracks = []
        self.current_index = 0
        self.is_playing = False

        # Загружаем все wav/mp3 файлы из папки
        if os.path.exists(music_folder):
            for f in os.listdir(music_folder):
                if f.endswith(('.wav', '.mp3', '.ogg')):
                    self.tracks.append(os.path.join(music_folder, f))

    def play(self):
        if not self.tracks:
            return
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play()

    def prev_track(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play()

    def get_track_name(self):
        if not self.tracks:
            return "No tracks found"
        return os.path.basename(self.tracks[self.current_index])

    def get_status(self):
        return "▶ Playing" if self.is_playing else "⏹ Stopped"
        