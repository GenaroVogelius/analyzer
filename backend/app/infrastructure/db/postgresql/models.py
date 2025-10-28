from tortoise import ForeignKeyFieldInstance, Model, fields


class TicketModel(Model):
    id = fields.IntField(unique=True, pk=True)
    species = fields.CharField(max_length=100, description="ESPE from dataset")
    species_code = fields.CharField(
        max_length=50, description="CodigoEspecie from dataset"
    )
    ticker = fields.CharField(
        max_length=25, null=True, description="Ticker from dataset"
    )

    class Meta:
        table = "tickets"


class OperationTypeModel(Model):
    id = fields.IntField(unique=True, pk=True)
    type_operation = fields.CharField(max_length=50, description="CPTE from dataset")

    class Meta:
        table = "operation_types"


class ReferenceModel(Model):
    id = fields.IntField(unique=True, pk=True)
    detail = fields.CharField(
        max_length=500, null=True, description="DETA from dataset"
    )

    class Meta:
        table = "references"


class OperationModel(Model):
    id = fields.IntField(
        unique=True, pk=True, generated=False, description="NUME from dataset"
    )
    type_operation: ForeignKeyFieldInstance = fields.ForeignKeyField(
        "models.OperationTypeModel",
        related_name="operations",
        on_delete=fields.CASCADE,
        description="CPTE from dataset",
    )
    amount = fields.IntField(description="CANT from dataset", null=True)
    code = fields.CharField(max_length=50, description="CLAV from dataset")
    ticket: ForeignKeyFieldInstance = fields.ForeignKeyField(
        "models.TicketModel",
        related_name="operations",
        on_delete=fields.CASCADE,
        description="ESPE from dataset",
    )
    accumulated = fields.FloatField(description="ACUM from dataset")
    import_of_operation = fields.FloatField(
        description="IMPO of operation from dataset", null=True
    )
    price_of_operation = fields.FloatField(
        description="PCIO of operation from dataset", null=True
    )
    number_receipt = fields.IntField(description="NroComprobante from dataset")
    comprobant_of_operation = fields.IntField(
        description="Comprobante of operation from dataset", null=True
    )
    date_liquidation = fields.DateField(description="FEC1 from dataset")
    date_operation = fields.DateField(description="FEC2 from dataset")
    reference: ForeignKeyFieldInstance = fields.ForeignKeyField(
        "models.ReferenceModel",
        related_name="operations",
        on_delete=fields.CASCADE,
        description="DETA from dataset",
    )

    class Meta:
        table = "operations"


# uv run aerich history
# aerich init-db
# # Ver migraciones pendientes
# uv run aerich heads

# # Revertir a la migración anterior
# uv run aerich downgrade

# # Revertir a una migración específica
# uv run aerich downgrade 0_20251009154616_init.py


# Aplicar todas las migraciones pendientes
# uv run aerich upgrade

# # Aplicar hasta una migración específica
# uv run aerich upgrade 1_20251009154811_add_index_to_ticket.py

# Crear una nueva migración después de cambiar modelos
# uv run aerich migrate --name "descripcion_del_cambio"
