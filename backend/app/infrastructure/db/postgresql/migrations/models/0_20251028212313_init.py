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
    "import_of_operation" DOUBLE PRECISION,
    "price_of_operation" DOUBLE PRECISION,
    "number_receipt" INT NOT NULL,
    "comprobant_of_operation" INT,
    "date_liquidation" DATE NOT NULL,
    "date_operation" DATE NOT NULL,
    "reference_id" INT NOT NULL REFERENCES "references" ("id") ON DELETE CASCADE,
    "ticket_id" INT NOT NULL REFERENCES "tickets" ("id") ON DELETE CASCADE,
    "type_operation_id" INT NOT NULL REFERENCES "operation_types" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "operations"."id" IS 'NUME from dataset';
COMMENT ON COLUMN "operations"."amount" IS 'CANT from dataset';
COMMENT ON COLUMN "operations"."code" IS 'CLAV from dataset';
COMMENT ON COLUMN "operations"."accumulated" IS 'ACUM from dataset';
COMMENT ON COLUMN "operations"."import_of_operation" IS 'IMPO of operation from dataset';
COMMENT ON COLUMN "operations"."price_of_operation" IS 'PCIO of operation from dataset';
COMMENT ON COLUMN "operations"."number_receipt" IS 'NroComprobante from dataset';
COMMENT ON COLUMN "operations"."comprobant_of_operation" IS 'Comprobante of operation from dataset';
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
    "eJztmm1vm0gQx7+K5VetlKtiX3yt7h0hROdr/CDHqU6qKrSGsb0KsHRZro0qf/furnkwjw"
    "GCg9PmnT07A7M/lv8sAz/6NjHB8t7NXKCIYeJMxP/+370ffQfZwH8UeJz1+sh143FhYGhl"
    "yRAS+kozWnmMIoPxkTWyPOAmEzyDYle4cKvjW5YwEoM7YmcTm3wHf/VBZ2QDbAuUD3z+ws"
    "3YMeE7eOFf915fY7DMRNrYFOeWdp09uNI2dti1dBRnW+kGsXzbiZ3dB7YlTuSNHSasG3DE"
    "bMA8yF+kF0w2NO1T5QZGfYhyNGODCWvkW+xgvgkI/endROutKbF7JmLIA3nyHCYGx8p58u"
    "w8OeGNOOkfw8HF+4sPf/518YG7yMQiy/vdfroxi32gJDJd9ndynJ9z7yGxxhyRTfw9iIos"
    "44BGPANaEc7QJeYZL6JyoKoyXXYGNAZo8Psji0/dIprPL/RP0eMpNlmNT8B3o3xqgs9G33"
    "ULnA3b8r+j8xJWn5SF+o+yeDM6fyuOTbhI7PVjGowM5VASJzIM3/YtiSBD9doiqGhZJuNS"
    "dNci8Hn5KurdpAHfEp5Xs7vLG603X2jq+HY8m4oD2g/eVyseFCZuwEzOeqEpNym82HYJZT"
    "pZ65GI18JcEN8Qd3tiMJ7MZz2y7kVZnR56l2IDmpPPD+8c/Fwdnzp4x7dXQHUKBvC8a5S6"
    "bGA7W4jmtKeUqMR2KVkhh8FJVL8wm0dWdiHkkiN0vcE4IP3EFd42dn5y0C0+Q2wW8L7iHv"
    "nA82JTpIULwza8Ez+ed4Vfa+qgZQlRlloevpLF+gi8skXaLbrh0dFRWAMFh5eiWk9g6bCu"
    "hfRKWyoncB8zbNwDq4cyEdM1R+123t1T7QFHPh7fljV55sV2zVWdL7viKlou6/vcZkESVc"
    "72lVDAG+cjPEjUY54b4vd8DtB012nJ7VHn6eQx78I1FFrjfQdF36JuVf7S4j/4PGG/XVWV"
    "W1W54iKbVYUW8C7lgTrg2lAWKnM9lMDHeUbFpwWki/BYHVBtWLSqUk3X6HywQh5WyLj/hq"
    "ipJ3RCjJAhSVki3+yQPbTTFuSgjWQipiISLxaKsiZ2Qk4qNLIDITz7pbrZwTU+QjO7mMEz"
    "d68fK0jFbdhsZOcN2YYl/wgN2cwWoPimj69F8q1Q8jpcBrHXHxdgFREvfBN18tegSGF3x5"
    "TEVCXKkcNsrSqWwkj8X1XwxamgCQxhq476xRGNVK+9HlvT5/CU6FVTvTLZ+711r+Wd5VF1"
    "7/ChJkf0Us88xYq3f4h4lbsXJ3eeCwaGnLutWO8OQrre5jXtmCUUb1BJ8QYlijc4z7x6Dy"
    "Dpdb9oSMd1TVglJt4QbZ/WieyoM+0dWuthJYrouFxLcaVPZjocVWA6HBUyFUO/cbVuubt2"
    "1GqtAMXGNq9QByOlNRrFPq8l+gWV6P+BejUbMgchHReQ6hRTolZN1cpkbZT5HI7fGjUgBu"
    "4vE+BRNjX8jAzyPnD993Y2LfoiJQpJgbxz+AQ/m9hgZz0Le+zLaWItoShmLZK2veAbqhDe"
    "m4nyX5qrejO7lBSIxzZUHkUe4LJe8W2/vOx+Ao+zKdo="
)
