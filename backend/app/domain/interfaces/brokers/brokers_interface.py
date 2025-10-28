from enum import StrEnum

class Broker(StrEnum):
    VETA_CAPITAL = "https://cuentas.vetacapital.com.ar"
    COCOS = "https://cocoscap.com"
    IEB = "https://clientesv2.invertirenbolsa.com.ar"

    @classmethod
    def is_valid_url(cls, url: str) -> bool:
        """
        Check if the provided URL is a valid Broker URL.

        :param url: The URL to check
        :return: True if the URL is valid, False otherwise
        """
        return any(broker.value == url for broker in cls)