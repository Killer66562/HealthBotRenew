from typing import Any, Self

from discord.ui import View, Button, Modal
from discord import ButtonStyle, Embed, Interaction

from . import factories, buttons
    

class ViewNode(View):
    def __init__(
            self, 
            prev_view: Self | None = None, 
            next_view: Self | None = None,
            embed: Embed | None = None,
            modal_factory: factories.TextInputModalFactory | None = None, 
            modal_next_view: Self | None = None, 
            *, 
            timeout: float | None = None):
        super().__init__(timeout=timeout)
        self._prev_view: Self | None = prev_view
        self._next_view: Self | None = next_view
        self._embed: Embed | None = embed
        self._modal_factory: factories.TextInputModalFactory | None = modal_factory
        self._modal_next_view: Self | None = modal_next_view
        self._answer: Any | None = None
        self._ans_view_map: dict[Any, Self] = dict()
        self._buttons_map: dict[str, buttons.Updatable] = dict()
        self._update_button_statuses()

    def _update_button_statuses(self):
        for key in self._buttons_map:
            self._buttons_map[key].update()

    def register_view(self, key: Any, view: Self) -> None:
        self._ans_view_map[key] = view
        self._update_button_statuses()

    def remove_view(self, key: Any) -> None:
        view = self._ans_view_map.get(key)
        if view is not None:
            self._ans_view_map.pop(key)
        self._update_button_statuses()

    def get_view(self, key: Any) -> Self | None:
        return self._ans_view_map.get(key)
    
    def register_button(self, key: str, button: buttons.ButtonWithAnswerView) -> None:
        self._buttons_map[key] = button
        self._update_button_statuses()

    def remove_button(self, key: str) -> None:
        button = self._buttons_map.get(key)
        if button is not None:
            self._buttons_map.pop(key)
        self._update_button_statuses()

    @property
    def prev_view(self):
        return self._prev_view
    
    @prev_view.setter
    def prev_view(self, view: Self | None):
        self._prev_view = view
        self._update_button_statuses()

    @property
    def next_view(self):
        return self._next_view
    
    @next_view.setter
    def next_view(self, view: Self | None):
        self._next_view = view
        self._update_button_statuses()

    @property
    def modal_factory(self):
        return self._modal_factory
    
    @modal_factory.setter
    def modal_factory(self, factory: factories.TextInputModalFactory | None):
        self._modal_factory = factory
        self._update_button_statuses()

    @property
    def modal_next_view(self):
        return self._modal_next_view
    
    @modal_next_view.setter
    def modal_next_view(self, view: Self | None):
        self._modal_next_view = view
        self._update_button_statuses()

    @property
    def answer(self) -> Any:
        return self._answer
    
    @answer.setter
    def answer(self, value: Any):
        self._answer = value
        self._update_button_statuses()

    @property
    def embed(self) -> Embed | None:
        return self._embed
    
    @embed.setter
    def embed(self, embed: Embed | None):
        self._embed = embed
        self._update_button_statuses()