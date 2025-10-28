from abc import abstractmethod
from typing import List, Protocol

from app.domain.entities.entities import Operation


class ResponseParserInterface(Protocol):
    """
    Interface for response parser.
    """

    @abstractmethod
    def parse(self, positions: List[Operation]) -> List[dict]:
        """
        Parse a list of Operation entities and convert them to response format.

        Args:
            positions: List of Operation entities

        Returns:
            List of response entities
        """
        raise NotImplementedError
