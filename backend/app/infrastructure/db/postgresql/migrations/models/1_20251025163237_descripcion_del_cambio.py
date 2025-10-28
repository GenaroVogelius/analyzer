from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "operations" ALTER COLUMN "date_liquidation" TYPE DATE USING "date_liquidation"::DATE;
        ALTER TABLE "operations" ALTER COLUMN "date_operation" TYPE DATE USING "date_operation"::DATE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "operations" ALTER COLUMN "date_liquidation" TYPE TIMESTAMPTZ USING "date_liquidation"::TIMESTAMPTZ;
        ALTER TABLE "operations" ALTER COLUMN "date_operation" TYPE TIMESTAMPTZ USING "date_operation"::TIMESTAMPTZ;"""


MODELS_STATE = (
    "eJztmttu2zgQhl/F8FULZIvYG2+LvVMUB5ttYgeOUyxQFAItjWUiEqlS1LZB4XcvSZ2sYy"
    "XVjpw2d9ZwRiQ/if+QY30butQCx38z94Ahjim5kdfDvwffhgS5IH5UeJwMhsjz0nZp4Gjl"
    "qBAa+yozWvmcIZOLljVyfBAmC3yTYU+6CCsJHEcaqSkcMbFTU0Dw5wAMTm3gG2Ci4eMnYc"
    "bEgq/gx5feg7HG4FiZYWNL9q3sBn/0lO2K8EvlKHtbGSZ1Apekzt4j31CSeGPCpdUGImcD"
    "1s745fCiycamcKjCwFkAyRit1GDBGgUO35lvBsJwdn8zHawZdQcW4sgH1XkJE1NgFTzF6H"
    "w1YVt2+sd4dPb27N2ff529Ey5qYInl7TacbsoiDFREZsvhVrWLPkMPhTXliFwahCAaskwD"
    "OvGMaCU4Y5eUZ/oS1QPVtdmyN6ApQFOsjyI+fYNYOb/YP0dPDLHL2/gT+K61D13wueir4Q"
    "Cx+UZcTk5rWH3QFvo/2uLV5PS1vDcVIhHqxyxqGaumLE5kmoEbOApBgeqlQ1HVa5mNy9Fd"
    "y8Cn5avp9zcd+NbwvJjfn19PB7eLqX51dzWfyRu6j/5nJ22UJmHAXM16MdWuc3hJ4K6AGQ"
    "xMEENtseyLgfuR0+6AZ4zq1PUYXSHC4QiUQHQOhiPmhS2VHYt0L4RHOd6y2Bxg6cKxC2/k"
    "j6dFfTnVR3t+l7XltAxfsrVoDS8TeVToxgdHx2ANDIgJRqttUT6s7xV9MV1qR7COOTYfgL"
    "dDmYnpm+P07ra/reYOR9GeLsuWPMti++aq3y774irPQeuH0h18FlXJpokywDZ5D48K9ZUY"
    "GxJrvgRo/ii4FPbkOHj0mLfxOxRbh8lpg6EvyRGy/NUSP8Q8Idw36dqdrl0IkS2qwh7wLt"
    "WNeuDaURYac92VwB/zTJLPHpAu4nv1QLVj0mpKNZ+jy8FKeVgh8+ELYpaR0QnZQsc0Z0l8"
    "i03u2M1bEEG2YiKnIgdeLRR1laWMnDSoLkVCePJLlZiiZ3yAClM1gycuKf0oIVXXRoqRvV"
    "dJOqb8A1RJCluA6kWfPotsqTb7HM6j2Mv3C3CqiFeWh4/+GVQp7PaQkpjLRCVyWMxV1VKY"
    "iP+LCj47FbSAI+y0Ub80opPq7a+y3vUcnhO9ZqpXJ3u/t+7teWd5UN3bPdSUiF7uzFOteO"
    "Eh4kXunp3c+R6YGEpWW7Xe7YT0vc3rWjHLKN6okeKNahRvdFr4PyyCZLT9mzEf1zdhnVrY"
    "ptNwWEeyoy6Ud1irw0oS0XO6VuLKfprpeNKA6XhSyVQ2/cbZes/VtYNmaw0YNjdliTpqqc"
    "3RKPV5SdHPKEX/D8xvWZDZCek5gTSnmBO1ZqpWJ2uTwjcqYmm0gBi5P0+AB9nUiB45lH11"
    "9u/dfFb12VQSkgN5T8QEP1rY5CcDB/v803FiraEoZy0H7frRxzwxvFc32n95rvr1/FxRoD"
    "63mbqLusF5u+S7//Sy/Q5im7dg"
)
