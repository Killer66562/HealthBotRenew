from __future__ import annotations

from discord.ui import Modal

from . import views, factories


class ModalWithViews(Modal):
    def __init__(
            self, 
            parent_view: views.ViewNode, 
            next_view: views.ViewNode, 
            *, 
            title: str = ..., 
            timeout: float | None = None, 
            custom_id: str = ...) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self._parent_view = parent_view
        self._next_view = next_view

    async def on_submit(self, interaction: views.Interaction) -> None:
        return await super().on_submit(interaction)
    

class TextInputModal(ModalWithViews):
    def __init__(
            self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: factories.TextInputFactory, 
            *, 
            title: str = ..., timeout: float | None = None, custom_id: str = ...) -> None:
        super().__init__(parent_view, next_view, title=title, timeout=timeout, custom_id=custom_id)
        self._text_input = text_input_factory.generate()
        self.add_item(self._text_input)

    @property
    def _answer(self) -> str:
        return self._text_input.value.strip()

    async def on_submit(self, interaction: views.Interaction) -> None:
        return await super().on_submit(interaction)
    

class AgeModal(TextInputModal):
    TITLE = "填寫年齡"
    CUSTOM_ID = "age"
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: factories.TextInputFactory, *, title: str = TITLE, timeout: float | None = None, custom_id: str = CUSTOM_ID) -> None:
        super().__init__(parent_view, next_view, text_input_factory, title=title, timeout=timeout, custom_id=custom_id)

    async def on_submit(self, interaction: views.Interaction) -> None:
        try:
            age_value = int(self._answer)
            if age_value < 0:
                raise ValueError()
            self._parent_view.answer = age_value
            return await interaction.response.edit_message(view=self._next_view, embed=self._next_view.embed)
        except ValueError:
            return await interaction.response.send_message(content="請輸入一個有效的正整數", ephemeral=True)


class BMIModal(TextInputModal):
    TITLE = "填寫BMI"
    CUSTOM_ID = "bmi"
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: factories.TextInputFactory, *, title: str = TITLE, timeout: float | None = None, custom_id: str = CUSTOM_ID) -> None:
        super().__init__(parent_view, next_view, text_input_factory, title=title, timeout=timeout, custom_id=custom_id)

    async def on_submit(self, interaction: views.Interaction) -> None:
        try:
            bmi_value = float(self._answer)
            self._parent_view.answer = bmi_value
            return await interaction.response.edit_message(view=self._next_view, embed=self._next_view.embed)
        except ValueError:
            return await interaction.response.send_message(content="請輸入一個有效的小數", ephemeral=True)
        

class HBA1CModal(TextInputModal):
    TITLE = "填寫糖化血色素"
    CUSTOM_ID = "hba1c"
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: factories.TextInputFactory, *, title: str = TITLE, timeout: float | None = None, custom_id: str = CUSTOM_ID) -> None:
        super().__init__(parent_view, next_view, text_input_factory, title=title, timeout=timeout, custom_id=custom_id)

    async def on_submit(self, interaction: views.Interaction) -> None:
        try:
            age_value = float(self._answer)
            if age_value < 0:
                raise ValueError()
            self._parent_view.answer = age_value
            return await interaction.response.edit_message(view=self._next_view, embed=self._next_view.embed)
        except ValueError:
            return await interaction.response.send_message(content="請輸入一個有效的小數", ephemeral=True)
        

class BlooadSugarModal(TextInputModal):
    TITLE = "填寫血糖值"
    CUSTOM_ID = "blood_sugar"
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: factories.TextInputFactory, *, title: str = TITLE, timeout: float | None = None, custom_id: str = CUSTOM_ID) -> None:
        super().__init__(parent_view, next_view, text_input_factory, title=title, timeout=timeout, custom_id=custom_id)

    async def on_submit(self, interaction: views.Interaction) -> None:
        try:
            age_value = float(self._answer)
            if age_value < 0:
                raise ValueError()
            self._parent_view.answer = age_value
            return await interaction.response.edit_message(view=self._next_view, embed=self._next_view.embed)
        except ValueError:
            return await interaction.response.send_message(content="請輸入一個有效的小數", ephemeral=True)