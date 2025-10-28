import datetime
from dataclasses import dataclass


@dataclass
class OperationType:
    type_operation: str  # CPTE


@dataclass
class Reference:
    detail: str | None = None  # DETA


@dataclass
class Ticket:
    species: str  # ESPE
    species_code: str  # CodigoEspecie
    ticker: str | None = None  # Ticker


@dataclass
class Operation:
    id: int  # NUME
    type_operation: OperationType
    ticket: Ticket
    code: str  # CLAV
    accumulated: float  # ACUM
    number_receipt: int  # NroComprobante
    date_liquidation: datetime.date  # FEC1
    date_operation: datetime.date  # FEC2
    reference: Reference  # DETA
    import_of_operation: float | None = None  # IMPO
    comprobant_of_operation: int | None = None  # Comprobante
    amount: float | None = None  # CANT
    price_of_operation: float | None = None  # PCIO

    @classmethod
    def from_model(cls, operation_model):
        """
        Create an Operation entity from a database model.
        """
        return cls(
            id=operation_model.id,
            type_operation=OperationType(
                type_operation=operation_model.type_operation.type_operation
            ),
            ticket=Ticket(
                species=operation_model.ticket.species,
                species_code=operation_model.ticket.species_code,
                ticker=operation_model.ticket.ticker,
            ),
            code=operation_model.code,
            accumulated=operation_model.accumulated,
            number_receipt=operation_model.number_receipt,
            date_liquidation=operation_model.date_liquidation,
            date_operation=operation_model.date_operation,
            reference=Reference(detail=operation_model.reference.detail),
            import_of_operation=operation_model.import_of_operation,
            comprobant_of_operation=operation_model.comprobant_of_operation,
            amount=operation_model.amount,
            price_of_operation=operation_model.price_of_operation,
        )


@dataclass
class OperationsAnalyzed:
    id: int
    ticker: str
    amount: int
    date_operation: datetime.date
    date_liquidation: datetime.date
    buy_price: float
    sell_price: float
    inverted_amount: float
    current_amount: float
    percentage_gain: float
    nominal_gain: float
    tna: float

    def to_formatted_dict(self) -> dict:
        """
        Convert to dictionary with formatted values:
        - Float values rounded to 2 decimal places
        - Dates formatted as DD/MM/YYYY
        """
        return {
            "id": self.id,
            "ticker": self.ticker,
            "amount": self.amount,
            "date_operation": self.date_operation.strftime("%d/%m/%Y"),
            "date_liquidation": self.date_liquidation.strftime("%d/%m/%Y"),
            "buy_price": round(self.buy_price, 2),
            "sell_price": round(self.sell_price, 2),
            "inverted_amount": round(self.inverted_amount, 2),
            "current_amount": round(self.current_amount, 2),
            "percentage_gain": round(self.percentage_gain, 2),
            "nominal_gain": round(self.nominal_gain, 2),
            "tna": round(self.tna, 2),
        }
