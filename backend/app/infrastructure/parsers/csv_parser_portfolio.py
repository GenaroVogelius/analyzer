from datetime import datetime

import pandas as pd
from fastapi import UploadFile

from app.domain.entities.entities import Operation, OperationType, Reference, Ticket
from app.domain.entities.enums import DataSetColumns
from app.domain.interfaces.parsers.csv_parser_interface import CsvParserInterface


class CsvParserPortfolio(CsvParserInterface):
    """
    Parser for csv files.
    """

    def _parse_date(self, date_string):
        """
        Parse date string from DD/MM/YY format to datetime object.
        """
        if pd.isna(date_string) or date_string is None:
            return None

        try:
            # Handle DD/MM/YY format
            if isinstance(date_string, str) and "/" in date_string:
                return datetime.strptime(date_string, "%d/%m/%y")
            # If it's already a datetime object, return as is
            elif isinstance(date_string, datetime):
                return date_string
            # Try pandas to_datetime as fallback
            else:
                return pd.to_datetime(date_string)
        except (ValueError, TypeError):
            return None

    def parse(self, csv_file: UploadFile) -> list[Operation]:
        """
        Parse a csv file.
        """
        df = pd.read_csv(csv_file.file, sep=",")

        # Replace all nan values with None
        df = df.replace([pd.NA, pd.NaT, float("nan")], None)

        operations = []
        for index, row in df.iterrows():
            operation = Operation(
                id=row[DataSetColumns.ID],
                type_operation=OperationType(
                    type_operation=row[DataSetColumns.TYPE_OPERATION]
                ),
                ticket=Ticket(
                    species=row[DataSetColumns.SPECIES],
                    species_code=row[DataSetColumns.SPECIES_CODE].strip() ,
                    ticker=row[DataSetColumns.TICKER].strip()
                ),
                amount=row[DataSetColumns.AMOUNT],
                code=row[DataSetColumns.CODE],
                accumulated=row[DataSetColumns.ACCUMULATED],
                number_receipt=row[DataSetColumns.NUMBER_RECEIPT],
                date_liquidation=self._parse_date(row[DataSetColumns.DATE_LIQUIDATION]),
                date_operation=self._parse_date(row[DataSetColumns.DATE_OPERATION]),
                reference=Reference(detail=row[DataSetColumns.REFERENCE]),
                import_of_operation=row[DataSetColumns.IMPO],
                price_of_operation=row[DataSetColumns.PCIO],
                comprobant_of_operation=row[DataSetColumns.COMPROBANTE],
            )
            operations.append(operation)
        return operations
