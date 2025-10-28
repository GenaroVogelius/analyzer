from abc import abstractmethod
from typing import Protocol

from fastapi import UploadFile

from app.domain.entities.entities import Operation


class CsvParserInterface(Protocol):
    """
    Interface for csv parser.
    """
    @abstractmethod
    def parse(self, csv_file: UploadFile) -> list[Operation]:
        """
        Parse a csv file.
        """
        raise NotImplementedError       

