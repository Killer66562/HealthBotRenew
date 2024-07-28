from __future__ import annotations

from abc import ABC, abstractmethod

from discord.ui import TextInput

from . import modals, views


class ModalWithViewsFactory(ABC):
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode) -> None:
        super().__init__()
        self._parent_view = parent_view
        self._next_view = next_view

    @abstractmethod
    def generate(self) -> modals.ModalWithViews:
        return modals.ModalWithViews(parent_view=self._parent_view, next_view=self._next_view)
    

class TextInputFactory(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def generate(self) -> TextInput: ...


class AgeInputFactory(TextInputFactory):
    def __init__(self) -> None:
        super().__init__()

    def generate(self) -> TextInput:
        return TextInput(label="年齡", placeholder="請輸入年齡（歲）")
    

class BMIInputFactory(TextInputFactory):
    def __init__(self) -> None:
        super().__init__()

    def generate(self) -> TextInput:
        return TextInput(label="BMI", placeholder="請輸入BMI")
    

class HBA1CInputFactory(TextInputFactory):
    def __init__(self) -> None:
        super().__init__()

    def generate(self) -> TextInput:
        return TextInput(label="糖化血色素", placeholder="請輸入糖化血色素（%）")
    

class BloodSugarInputFactory(TextInputFactory):
    def __init__(self) -> None:
        super().__init__()

    def generate(self) -> TextInput:
        return TextInput(label="血糖值", placeholder="請輸入血糖值")


class TextInputModalFactory(ModalWithViewsFactory):
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: TextInputFactory) -> None:
        super().__init__(parent_view, next_view)
        self._text_input_factory = text_input_factory

    def generate(self) -> modals.TextInputModal:
        return modals.TextInputModal(parent_view=self._parent_view, next_view=self._next_view, text_input_factory=self._text_input_factory)

    
class AgeModalFactory(TextInputModalFactory):
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: TextInputFactory) -> None:
        super().__init__(parent_view, next_view, text_input_factory)

    def generate(self) -> modals.AgeModal:
        return modals.AgeModal(parent_view=self._parent_view, next_view=self._next_view, text_input_factory=self._text_input_factory)
    

class BMIModalFactory(TextInputModalFactory):
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: TextInputFactory) -> None:
        super().__init__(parent_view, next_view, text_input_factory)

    def generate(self) -> modals.BMIModal:
        return modals.BMIModal(parent_view=self._parent_view, next_view=self._next_view, text_input_factory=self._text_input_factory)

  
class HBA1CModalFactory(TextInputModalFactory):
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: TextInputFactory) -> None:
        super().__init__(parent_view, next_view, text_input_factory)

    def generate(self) -> modals.HBA1CModal:
        return modals.HBA1CModal(parent_view=self._parent_view, next_view=self._next_view, text_input_factory=self._text_input_factory)


class BloodSugarModalFactory(TextInputModalFactory):
    def __init__(self, parent_view: views.ViewNode, next_view: views.ViewNode, text_input_factory: TextInputFactory) -> None:
        super().__init__(parent_view, next_view, text_input_factory)

    def generate(self) -> modals.BlooadSugarModal:
        return modals.BlooadSugarModal(parent_view=self._parent_view, next_view=self._next_view, text_input_factory=self._text_input_factory)