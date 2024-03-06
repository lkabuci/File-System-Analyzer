from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

PathLike = Union[Path, str]


class AnalyserInterface(ABC):
    @abstractmethod
    def add(self, filepath: PathLike):
        """
        Abstract method to add a file to the analyzer.
        """
        pass

    @abstractmethod
    def report(self):
        """
        Abstract method to report the results of the analysis.
        """
        pass
