import pygame
import os

class Assats:

    def __init__(self) -> None:
        self._images = {}

    def load_image(self, image_path: str, name: str) -> None:
        image = pygame.image.load(image_path)
        self._images[name] = image

    def load_art_folder(self, folder_path: str) -> None:
        EXCEPTIONS = set()

        for file in os.listdir(folder_path):
            if file.endswith(".png") and not any(file.startswith(exception) for exception in EXCEPTIONS):
                self.load_image(f"{folder_path}/{file}", file)

    def get_image(self, name: str) -> None:
        return self._images[name]