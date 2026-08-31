from .framework import Game, Assats
from .entities.general.content_manager import ContentManager
from .entities.main_menu.main_menu import MainMenu
from .entities.content.loader import load_content

class GardenRunner(Game):

    def __init__(self) -> None:
        super().__init__(title="Garden Runner", background_color="lightblue")
        self.content_manager = ContentManager()
        self.asset_manager: Assats = Assats()

        self.asset_manager.load_art_folder("game/art")
        load_content(self.content_manager)

        self.add_entity(MainMenu())