import importlib
import os

EXCEPTIONS = ["loader", "__init__"]

def load_content(content_manager):
    for file in os.listdir("game/entities/content"):
        if file.endswith(".py") and not any(file.startswith(exception) for exception in EXCEPTIONS):
            module = importlib.import_module(f"game.entities.content.{file[:-3]}")
            if hasattr(module, "register"):
                module.register(content_manager)