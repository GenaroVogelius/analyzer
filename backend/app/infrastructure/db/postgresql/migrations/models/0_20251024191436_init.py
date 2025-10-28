from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "operation_types" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type_operation" VARCHAR(50) NOT NULL
);
COMMENT ON COLUMN "operation_types"."type_operation" IS 'CPTE from dataset';
CREATE TABLE IF NOT EXISTS "references" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "detail" VARCHAR(500)
);
COMMENT ON COLUMN "references"."detail" IS 'DETA from dataset';
CREATE TABLE IF NOT EXISTS "tickets" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "species" VARCHAR(100) NOT NULL,
    "species_code" VARCHAR(50) NOT NULL,
    "ticker" VARCHAR(25)
);
COMMENT ON COLUMN "tickets"."species" IS 'ESPE from dataset';
COMMENT ON COLUMN "tickets"."species_code" IS 'CodigoEspecie from dataset';
COMMENT ON COLUMN "tickets"."ticker" IS 'Ticker from dataset';
CREATE TABLE IF NOT EXISTS "operations" (
    "id" INT NOT NULL PRIMARY KEY,
    "amount" INT,
    "code" VARCHAR(50) NOT NULL,
    "accumulated" DOUBLE PRECISION NOT NULL,
    "number_receipt" INT NOT NULL,
    "date_liquidation" TIMESTAMPTZ NOT NULL,
    "date_operation" TIMESTAMPTZ NOT NULL,
    "reference_id" INT NOT NULL REFERENCES "references" ("id") ON DELETE CASCADE,
    "ticket_id" INT NOT NULL REFERENCES "tickets" ("id") ON DELETE CASCADE,
    "type_operation_id" INT NOT NULL REFERENCES "operation_types" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "operations"."id" IS 'NUME from dataset';
COMMENT ON COLUMN "operations"."amount" IS 'CANT from dataset';
COMMENT ON COLUMN "operations"."code" IS 'CLAV from dataset';
COMMENT ON COLUMN "operations"."accumulated" IS 'ACUM from dataset';
COMMENT ON COLUMN "operations"."number_receipt" IS 'NroComprobante from dataset';
COMMENT ON COLUMN "operations"."date_liquidation" IS 'FEC1 from dataset';
COMMENT ON COLUMN "operations"."date_operation" IS 'FEC2 from dataset';
COMMENT ON COLUMN "operations"."reference_id" IS 'DETA from dataset';
COMMENT ON COLUMN "operations"."ticket_id" IS 'ESPE from dataset';
COMMENT ON COLUMN "operations"."type_operation_id" IS 'CPTE from dataset';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztml1v2zYUhv+K4asMyIrYS9pid4qioF5jO7CVbmhRCLR0bBORSJWilgaF//tIWh/Wl2"
    "upduQsubMOzxHJh+R7SFo/uh51wA3ejH1giGNKhvK5+2fnR5cgD8SPCo/TThf5flouDRzN"
    "XBVCY19lRrOAM2RzUTJHbgDC5EBgM+xLF2EloetKI7WFIyaL1BQS/C0Ei9MF8CUwUfDlqz"
    "Bj4sB3COJH/96aY3CdTLOxI+tWdos/+so2IPxaOcraZpZN3dAjqbP/yJeUJN6YcGldAJG9"
    "AWej/bJ5UWdj07qpwsBZCEkbndTgwByFLt/obwZCd3Q3NDpzRr2OgzgKQFVewsQWWAVP0b"
    "pAdXghK/293zt/d/7+j7fn74WLalhiebdadzdlsQ5UREZmd6XKRZ1rD4U15Yg8Gq5B7Mgy"
    "DWjEM6KV4IxdUp7pJNoOVNdGZmtAU4C2WB9FfPoSsXJ+sX+Onmhik9n4C/hutE9N8Hnou+"
    "UCWfCleLw428LqkzbRP2iTk4uz3+S7qRCJtX6MopK+KsriRLYdeqGrEBSoXrsUVU3LbFyO"
    "7lwGPi1fTb8bNuC7hefV+O7yxujcTgx9MB2MR/KF3mPwzU0LpUkYMFe9nhjaTQ4vCb0ZMI"
    "uBDaKpNZZ9MXA/ctoc8IhRnXo+ozNEOByBEojKwXJFv7CjsmOR7pXw4NiDcsRl8TnITvSC"
    "N/GPp0V+bei9/c5pczA0pqY2vFWTOYgns2YasqSfneKR9eRtTk+Sl3T+HpgfOvKx83k8Uq"
    "vBpwFfMFVj6md+7so2oZBTi9AHCzmbFGJzbCoOcrIBajTEmeijG+D+Cx9gBnNgQGywam0x"
    "82Ftq+OVYWpHoIkc2/fA66HMxLTN0Zjetrdt3+AoylPhqMmzLLZtrvqt2RZXeaac35eehr"
    "KoSjaglAFekI/wqFAPRNuQWPMlQPPHalPYk6P10WNexXMotnaTkxtDD8lxvHxqiR+in7De"
    "g+raVNeujG6JKuwBr6le1ALXhrKwM9dNCfw5zyT57AHpJH5XC1QbJq1dqeZzdDlYKQ8zZN"
    "8/IOZYGZ2QJbRPc5bEt1jk9b28BRG0UExkV2TDq4Vi2y1dRk52uKmLhPD0f3VdF43xAW7r"
    "qhk88fXczxJS9T1TMbL1G6eGKf8AN06FLUD1ok/HInvtnR2Hyyj2+uME3CrilVftRz8GVQ"
    "q7OqQk5jJRiRwWc1W1FCbi/6qCz04FHeAIu3XUL41opHr7+5ei6Tk8J3q7qd422XvZurfn"
    "neVBdW/zUFMierkzT7XirQ8Rr3L37OQu8MHGULLaqvVuI6TtbV7TG7OM4vV2UrzeFsXrnR"
    "X+W4wgWXX/ss3HtU1Ypw5eUGPdrCPZUReud1itw0oS0XK6VuLKfplp/2IHpv2LSqay6AVn"
    "6z3frh00W2vAsL0sS9RRydYcjVKf1xT9jFL0v8CCmhcyGyEtJ5DdKeZEbTdV2yZrF4Xvfc"
    "TSqAExcn+eAA+yqRE1cij7gu+v6XhU9QlaEpIDeUdEB7842OanHRcH/OtxYt1CUfY686lB"
    "DO9kqP2T56rfjC/z3xDIF1zWS777Ty+r/wBINRrh"
)
