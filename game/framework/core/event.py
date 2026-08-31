# from .entity import Entity
from collections.abc import Callable
from typing import Any
import warnings
#from ..warnings import EventDoesNotExistWarning

class EventSystem:

    def __init__(self) -> None:
        self.event_bus: dict[str, list[Callable]] = {}

    def add_event(self, event_name: str) -> None:
        if event_name in self.event_bus.keys():
            return

        self.event_bus[event_name] = []

    def remove_event(self, event_name: str) -> None:
        if not event_name in self.event_bus.keys():
            return

        del self.event_bus[event_name]

    def add_callback_function(self, event_name: str, callback_function: Callable) -> None:
        if not event_name in self.event_bus.keys():
            self.add_event(event_name)
            #warnings.warn(
            #    f"The event {event_name} where the listner was added does not exist, so it was created.",
            #    EventDoesNotExistWarning,
            #    stacklevel=2,
            #)
        self.event_bus[event_name].append(callback_function)

    def remove_callback_function(self, event_name: str, callback_function: Callable) -> None:
        if not event_name in self.event_bus.keys():
            return
        if not callback_function in self.event_bus[event_name]:
            return

        self.event_bus[event_name].remove(callback_function)

    def trigger_event(self, event_name: str, event: Any) -> None:
        if not event_name in self.event_bus.keys():
            #print("alsdfkj")
            self.add_event(event_name)
            #warnings.warn(
            #    f"The triggered event {event_name} does not exist, it was created.",
            #    EventDoesNotExistWarning,
            #    stacklevel=2,
            #)
        for callback_function in self.event_bus[event_name]:
            callback_function(event)