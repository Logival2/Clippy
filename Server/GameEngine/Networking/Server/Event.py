#!/usr/bin/env python3
"""Base Event class for Clippy"""
from inspect import iscoroutinefunction
from Utils.Serializable import Serializable
from Utils.Logger import logger


class Event(Serializable):
    """Base Event class to extend"""

    def __init__(self, type: str, *args, **kwargs):
        self.type: str = type
        self.handler_args: list = [*args]
        self.handler_kwargs: dict = kwargs


class BaseEventHandler:
    """Base event handler to extend"""

    def __init__(self):
        self.__event_handlers = {}

    def registerHandler(self, event_type, handler) -> None:
        """Registers a handler for a type of event"""
        # TODO: handle case when handler is already defined
        logger.info(f"Registering a handler for events of type {event_type}")
        if not callable(handler):
            raise TypeError(f"'{handler.__class__.__name__}' object is not callable")
        self.__event_handlers[event_type] = handler

    async def handle(self, event: Event, **kwargs):
        """
        Asynchronously invokes the handler function for this event
        Note: this function must be awaited
        """
        logger.debug(f"handling {event.type} event with args={event.handler_args} and kwargs {event.handler_kwargs}.")
        if event.type not in self.__event_handlers:
            logger.error(f"Event of type {event.type} received but no handler registered for that type")
            return None
        if iscoroutinefunction(self.__event_handlers[event.type]):
            return await self.__event_handlers[event.type](*event.handler_args, **dict(event.handler_kwargs, **kwargs))
        return self.__event_handlers[event.type](*event.handler_args, **dict(event.handler_kwargs, **kwargs))

        def hasHandler(self, event_type: str) -> bool:
            """Checks if a handler was registered for event_type"""
            return event_type in self.__event_handlers
