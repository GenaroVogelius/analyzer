from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "operations" ALTER COLUMN "import_of_operation" DROP NOT NULL;
        ALTER TABLE "operations" ALTER COLUMN "price_of_operation" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "operations" ALTER COLUMN "import_of_operation" SET NOT NULL;
        ALTER TABLE "operations" ALTER COLUMN "price_of_operation" SET NOT NULL;"""


MODELS_STATE = (
    "eJztmttu2zgQhl/F8FULZIvYG2+LvVMUBettfIDjFAsUhUBLY5uIJKoUtW1Q+N1L0jpYx0"
    "iKHDlt7uzhjDT8TP5DjfWjbxMTLO/dzAWKGCbORHzv/9370XeQDfxDgcdZr49cNx4XBoZW"
    "lgwhoa80o5XHKDIYH1kjywNuMsEzKHaFC7c6vmUJIzG4I3Y2scl38FcfdEY2wLZA+cDnL9"
    "yMHRO+gxd+de/1NQbLTKSNTXFvadfZgyttY4ddS0dxt5VuEMu3ndjZfWBb4kTe2GHCugFH"
    "zAbMg/xFesFkQ9M+VW5g1IcoRzM2mLBGvsUO5puA0J/eTbTemhK7ZyKGPJA3z2FicKycJ8"
    "/OkxPeiJv+MRxcvL/48OdfFx+4i0wssrzf7acbs9gHSiLTZX8nx/k99x4Sa8wR2cTfg6jI"
    "Mg5oxDOgFeEMXWKe8SIqB6oq02VnQGOABt8fWXzqFtF8fqF/ih5PsclqfAK+G+VTE3w2+q"
    "5b4GzYln8dnZew+qQs1H+UxZvR+VtxbcJFYq8f02BkKIeSOJFh+LZvSQQZqtcWQUXLMhmX"
    "orsWgc/LV1HvJg34lvC8mt1d3mi9+UJTx7fj2VRc0H7wvlrxoDBxA2Zy1gtNuUnhxbZLKN"
    "PJWo9EvBbmgviGuNsTg/FkPuuRdS/K6vTQuxQb0Jx8fnjn4Ofq+NTBO769AqpTMIDnXaPU"
    "ZQPbOUI0pz2lRCW2S8kKOQxOovqF2Tyysgshl1yha9qHqJ+4xNvmzm8OusVniM0C4FfcI5"
    "94XmwKtXBh2IZ34sPzQr/W1EHLGqIstTx8Jav1EXhlq7RbdMOjo6OwBgoOr0W1HsHSYV3v"
    "7SttqZzAPmbYuAdWD2UipmuO2u28u8faA458PN6WNXnmxXbNVZ0vu+Iqei7r+9xuQRJVzv"
    "mVUMAb5yM8SNRjnhviez4HaLrttOT2qPV08ph34RoKrf3oTE3Rt6hdlb+0+Ac+T9ifV1Xl"
    "VlWuuMhmVaEFvEt5oQ64NpSFylwPJfBxnlHxaQHpIrxWB1QbFq2qVNM1Oh+skIcVMu6/IW"
    "rqCZ0QI2RIUpbINztkD+20BTloI5mIqYjEi4WirIudkJMKnexACM9+qXZ28BsfoZtdzOCZ"
    "29ePFaTiPmw2svOObMOSf4SObOYIULzp498i+bdQ8ne4DGKvPy7AKiJe+FfUyf8GRQq7O6"
    "YkpipRjhxma1WxFEbi/6qCL04FTWAIW3XUL45opHrt9Y+bPoenRK+a6pXJ3u+tey2fLI+q"
    "e4cPNTmil3rmKVa8/UPEq9y9OLnzXDAw5Oy2Yr07COn6mNe0Y5ZQvEElxRuUKN7gPPPfew"
    "BJr/tKQzqua8IqMfGGaPu0TuREnWnv0FoPK1FEx+Vaiit9MtPhqALT4aiQqRj6jat1y921"
    "o1ZrBSg2tnmFOhgprdEo9nkt0S+oRP8P1KvZkDkI6biAVKeYErVqqlYma6PM+3B8a9SAGL"
    "i/TIBHOdTwOzLIe8P139vZtOiVlCgkBfLO4RP8bGKDnfUs7LEvp4m1hKKYtUja9oKXqEJ4"
    "bybKf2mu6s3sUlIgHttQeRV5gct6xbf98rL7CZ1jKiU="
)
