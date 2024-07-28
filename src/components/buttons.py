from __future__ import annotations

from typing import Any
from abc import ABC, abstractmethod

from discord import ButtonStyle, Emoji, PartialEmoji
from discord.ui import Button

from . import views


class Updatable(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def update(self): ...


class ButtonWithAnswerView(Button):
    def __init__(self, answer_view: views.ViewNode, answer: Any | None = None, *, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None, sku_id: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row, sku_id=sku_id)
        self._answer_view = answer_view
        self._answer = answer

    async def callback(self, interaction: views.Interaction) -> Any:
        next_view = self._answer_view.get_view(self._answer)
        if not next_view:
            return await interaction.response.send_message("This answer is not avaliable!", ephemeral=True)
        self._answer_view.answer = self._answer
        self._answer_view.next_view = next_view
        return await interaction.response.edit_message(view=next_view, embed=next_view.embed)


class PrevPageButton(ButtonWithAnswerView, Updatable):
    def __init__(self, answer_view: views.ViewNode, answer: Any | None = None, *, style: ButtonStyle = ButtonStyle.green, label: str | None = "上一頁", disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None, sku_id: int | None = None):
        super().__init__(answer_view, answer, style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row, sku_id=sku_id)

    def update(self):
        if self._answer_view.prev_view is None:
            self.disabled = True
        else:
            self.disabled = False

    async def callback(self, interaction: views.Interaction) -> Any:
        return await interaction.response.edit_message(view=self._answer_view.prev_view, embed=self._answer_view.prev_view.embed)
    

class NextPageButton(ButtonWithAnswerView, Updatable):
    def __init__(self, answer_view: views.ViewNode, answer: Any | None = None, *, style: ButtonStyle = ButtonStyle.green, label: str | None = "下一頁", disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None, sku_id: int | None = None):
        super().__init__(answer_view, answer, style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row, sku_id=sku_id)

    def update(self):
        if self._answer_view.next_view is None:
            self.disabled = True
        else:
            self.disabled = False

    async def callback(self, interaction: views.Interaction) -> Any:
        return await interaction.response.edit_message(view=self._answer_view.next_view, embed=self._answer_view.next_view.embed)
    

class CallModalButton(ButtonWithAnswerView, Updatable):
    def __init__(self, answer_view: views.ViewNode, answer: Any | None = None, *, style: ButtonStyle = ButtonStyle.blurple, label: str | None = "填寫表單", disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None, sku_id: int | None = None):
        super().__init__(answer_view, answer, style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row, sku_id=sku_id)

    def update(self):
        if self._answer_view.modal_factory is None:
            self.disabled = True
        else:
            self.disabled = False

    async def callback(self, interaction: views.Interaction) -> Any:
        if self._answer_view.modal_factory is None:
            return await interaction.response.send_message(content="Cannot send modal!", ephemeral=True)
        modal = self._answer_view.modal_factory.generate()
        return await interaction.response.send_modal(modal)
    

class DiabetesCheckAnswerButton(ButtonWithAnswerView, Updatable):
    def __init__(self, start_view: views.ViewNode, predicter, answer_view: views.ViewNode, answer: Any | None = None, *, style: ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | Emoji | PartialEmoji | None = None, row: int | None = None, sku_id: int | None = None):
        super().__init__(answer_view, answer, style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row, sku_id=sku_id)
        self._start_view = start_view
        self._predicter = predicter
        self.__collected_values = list()

    def __collect_values(self):
        values = list()
        current_view = self._start_view
        while current_view is not None and current_view is not self:
            if current_view.answer is None:
                break
            values.append(current_view.answer)
            current_view = current_view.next_view
        self.__collected_values = values

    def update(self):
        self.__collect_values()
        if len(self.__collected_values) != self._predicter.required_values_len:
            self.disabled = True
        else:
            self.disabled = False

    async def callback(self, interaction: views.Interaction) -> Any:
        result = self._predicter.predict(self.__collected_values)
        return await super().callback(interaction)