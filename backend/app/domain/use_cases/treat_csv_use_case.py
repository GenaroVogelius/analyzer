from app.domain.interfaces.parsers.csv_parser_interface import CsvParserInterface
from app.domain.interfaces.repositories.operations_repository_interface import (
    OperationsRepositoryInterface,
)


class TreatCsvUseCase:
    """
    This use case is responsible for treating the csv file in order to save it on the database.
    """

    def __init__(
        self, repository: OperationsRepositoryInterface, csv_parser: CsvParserInterface
    ):
        self.repository = repository
        self.csv_parser = csv_parser

    async def execute(self, csv_file):
        try:
            operations = self.csv_parser.parse(csv_file)
            operations_created = await self.repository.create_operations(operations)
            return operations_created
        except ValueError as e:
            # Re-raise ValueError with more context
            raise ValueError(f"CSV processing failed: {str(e)}")
        except Exception as e:
            # Handle any other unexpected errors
            raise ValueError(f"Unexpected error processing CSV file: {str(e)}")
