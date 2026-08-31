class ContentManager:

    def __init__(self) -> None:
        self.obstacle_types = set()

    def add_obstacle_type(self, type: type) -> None:
        self.obstacle_types.add(type)