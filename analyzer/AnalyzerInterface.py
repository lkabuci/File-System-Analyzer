from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

PathLike = Union[Path, str]


class AnalyserInterface(ABC):
    @abstractmethod
    def add(self, filepath: PathLike):
        """
        Absrtact method to add a file to the analyser.
        """
        pass

    @abstractmethod
    def report(self):
        """
        Abstract method to report the results of the analysis.
        """
        pass
