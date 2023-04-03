from __future__ import annotations
from abc import ABC, abstractmethod


class BuilderDialogFields(ABC):

    @abstractmethod
    def create_dialog(self, geometry: tuple):
        pass

    @abstractmethod
    def header(self):
        pass

    @abstractmethod
    def fields_space(self):
        pass

    @abstractmethod
    def massage(self):
        pass

    @abstractmethod
    def buttons(self):
        pass




