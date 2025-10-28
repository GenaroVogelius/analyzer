from abc import abstractmethod
from typing import Protocol

import pandas as pd

from app.core.enums import HomeBrokerTicketsType
from app.interfaces.brokers.brokers_interface import Broker


class HomeBrokerInterface(Protocol):
    dni: str
    username: str
    password: str
    url: str

    def __init__(
        self, dni: str, username: str, password: str, url: str = Broker.VETA_CAPITAL
    ):
        """
        Constructor for HomeBrokerInterface.

        :param dni: User's DNI
        :param username: account username
        :param password: account password
        :param url: Broker API URL (default to Vetacapital)
        :raises ValueError: If the provided URL is not a valid Broker URL
        """
        ...

    @abstractmethod
    async def login(self):
        pass

    @abstractmethod
    async def get_account_id(self):
        pass

    @abstractmethod
    async def get_current_portfolio(self, type_of_tickets: HomeBrokerTicketsType):
        pass

    @abstractmethod
    async def get_historical_portfolio(self, start_date: str, end_date: str) -> pd.DataFrame:
        pass

    @abstractmethod
    async def _make_request(self, url: str, payload: dict, headers: dict):
        pass
