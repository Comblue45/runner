from .entity import Entity

class TagSystem:
    def __init__(self) -> None:
        self.tags: dict[str, list[Entity]] = {}

    def add_tag(self, tag: str) -> None:
        if tag in self.tags.keys():
            return

        self.tags[tag] = []

    def remove_tag(self, tag: str) -> None:
        if not tag in self.tags.keys():
            return

        del self.tags[tag]

    def add_entity_to_tag(self, tag: str, entity: Entity) -> None:
        if not tag in self.tags.keys():
            self.add_tag(tag)

        if entity in self.tags[tag]:
            return

        self.tags[tag].append(entity)

    def get_by_tag(self, tag: str) -> list[Entity]:
        # Add "get by tags" (plural) function later 
        if not tag in self.tags.keys():
            self.add_tag(tag)
        return self.tags[tag]

    def get_all_tags(self) -> list[str]:
        return list(self.tags.keys())

    def remove_entity(self, entity: Entity) -> None:
        for tag in entity.tags:
            if not tag in self.tags.keys():
                continue
            if not entity in self.tags[tag]:
                continue

            self.tags[tag].remove(entity)