from __future__ import annotations
from abc import ABC, abstractmethod


class BuilderWidget(ABC):
    """
    Интерфейс Строитель виджета. Состоит из трех основных методов постройки объекта-виджета для списков.
    create_frame-основная форма виджета
    h_lay_upper - верхний(крайний левый) слой
    h_lay_middle - средний слой
    h_lay_lower -  последний слой
    """
    @abstractmethod
    def create_frame(self, scroll_area):
        pass

    @abstractmethod
    def h_lay_upper(self):
        pass

    @abstractmethod
    def h_lay_middle(self):
        pass

    @abstractmethod
    def h_lay_lower(self):
        pass
