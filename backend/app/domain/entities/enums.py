from enum import StrEnum


class DatabaseTypes(StrEnum):
    """Supported database types"""

    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"

class DataSetColumns(StrEnum):
    """
    Reference of the column values that comes from DataSet
    """
    ID = "NUME"
    TYPE_OPERATION = "CPTE"
    SPECIES = "ESPE"
    SPECIES_CODE = "CodigoEspecie"
    TICKER = "Ticker"
    AMOUNT = "CANT"
    CODE = "CLAV"
    ACCUMULATED = "ACUM"
    NUMBER_RECEIPT = "NroComprobante"
    DATE_LIQUIDATION = "FEC1"
    DATE_OPERATION = "FEC2"
    REFERENCE = "DETA"
    IMPO = "IMPO"
    PCIO = "PCIO"
    COMPROBANTE = "Comprobante"


class DatabaseColumnsOperations(StrEnum):
    """
    Reference of columns for database operations
    """

    # Include all OperationsColumns values
    TICKER = "ticker"
    AMOUNT = "amount"
    PRICE = "price"
    ACCUMULATED = "accumulated"
    NUMBER_RECEIPT = "number_receipt"
    TYPE_OPERATION = "type_operation"
    DATE_OPERATION = "date_operation"
    DATE_LIQUIDATION = "date_liquidation"

class OperationsAnalyzedColumns(StrEnum):
    """
    Reference of columns of operations made
    """
    TICKER = "ticker"
    BUY_PRICE = "buy_price"
    SELL_PRICE = "sell_price"
    BUY_DATE = "buy_date"
    SELL_DATE = "sell_date"
    INVERTED_AMOUNT = "inverted_amount"
    AMOUNT = "amount"
    PERCENTAGE_GAIN = "percentage_gain"
    NOMINAL_GAIN = "nominal_gain"
    TNA = "tna"

class HBTypeOperations(StrEnum):
    """
    Reference of the type operations that comes from Home Broker
    """
    BUY = "CPRA"
    SELL = "VTAS"
    SPECIES = "ESPE"
    SELL_PARITY = "VTU$"
    RECEIPT = "COBR"
    PAYMENT_ORDER = "PAGO"
    DEBIT_FOR_GARANTIES = "DGIP"
    CREDIT_FOR_GARANTIES = "EGIP"
    CREDIT_INDEX = "NCIN"
    BUY_INDEX = "CMIN"
    SELL_INDEX = "VTIN"
    DEBIT_INDEX = "DEIN"
    DIVIDEND = "DIV"
    BUY_TRADING_INDEX = "CTIN"
    CREDIT_MARKET_RIGHT = "DEME"
    SELL_TRADING = "VTTR"
    BUY_TRADING = "COTR"
    DEBT_NOTE = "DECU"
    SECURITY_TAKER_TERM = "TOCT"
    CASH_SURETY_TAKER = "TCCD"
    RENT_AND_AMORTIZATION = "RTA"
    PURCHASE_FOR_EXERCISE_PREMIUMS = "EJPC"
    SELL_PREMIUMS = "VTPR"
    BUY_PREMIUMS = "COPR"



class TypeOfSort(StrEnum):
    """
    Reference of the type of sort
    """
    ASCENDING = "ascending"
    DESCENDING = "descending"


