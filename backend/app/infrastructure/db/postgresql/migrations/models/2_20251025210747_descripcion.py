from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "operations" ADD "price_of_operation" DOUBLE PRECISION NOT NULL;
        ALTER TABLE "operations" ADD "import_of_operation" DOUBLE PRECISION NOT NULL;
        ALTER TABLE "operations" ADD "comprobant_of_operation" INT NOT NULL;
        COMMENT ON COLUMN "operations"."price_of_operation" IS 'PCIO of operation from dataset';
COMMENT ON COLUMN "operations"."import_of_operation" IS 'IMPO of operation from dataset';
COMMENT ON COLUMN "operations"."comprobant_of_operation" IS 'Comprobante of operation from dataset';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "operations" DROP COLUMN "price_of_operation";
        ALTER TABLE "operations" DROP COLUMN "import_of_operation";
        ALTER TABLE "operations" DROP COLUMN "comprobant_of_operation";"""


MODELS_STATE = (
    "eJztmttu2zgQhl/F8FULZIvYG2+LvVMUB+ttfIDjFAsUhUBLY5mIJKoUtW1Q+N1LUifrGE"
    "mxI6fNnT2cEclP5D/USD/6NjHA8t7NXaCIYeJMxf/+370ffQfZwH+UeJz1+sh1k3ZhYGht"
    "yRAS+UozWnuMIp3xlg2yPOAmAzydYle4cKvjW5YwEp07YsdMTL6Dv/qgMWIC2wLlDZ+/cD"
    "N2DPgOXvTXvdc2GCwjNWxsiL6lXWMPrrRNHHYtHUVva00nlm87ibP7wLbEib2xw4TVBEfM"
    "Boy98YvhhZONTMFQuYFRH+IxGonBgA3yLbY33xSE/uxuOu5tKLF7BmLIA9l5AROdY+U8+e"
    "g8OWFTdPrHcHDx/uLDn39dfOAucmCx5f0umG7CIgiURGar/k628z4DD4k14Yhs4gcgarJM"
    "AlrxDGnFOCOXhGeyiKqBqsps1RnQBKDO90cen7pFtJhf5J+hx4fYZjU+Ad+N8qkNPht91y"
    "xwTLblf0fnFaw+KUv1H2X5ZnT+VlybcJEI9GMWtgxlUxon0nXf9i2JIEf12iKobFmm4zJ0"
    "NyLwefkq6t20Bd8Knlfzu8ubcW+xHKuT28l8Ji5oP3hfraRRmLgBMznr5Vi5yeDFtkso08"
    "hGi0W8EeaS+O5xT6aLeY9sevGwTo+9S7EO7dEXh3dPfqFOTp2849troBoFHfi4GyS7fOBh"
    "DhHtac8oUYntUrJGDoOTyH/RaB5Z2qWQK67QNe191E9c4ofmzjsHzeIzxEYJ8CvuUUy8KD"
    "aDWrgwbMM78eN5oV+P1cGBNURZjYvwVazWR+BVrdJu0Q2Pjo7CBig4PBk1egjLhnW9t6/G"
    "K+UE9jHD+j2wZihTMV1zHN8uunuw3ePI25Nt2ZBnUWzXXNXFqiuuouqyuS+sF6RRFRxgCQ"
    "VsOh/hQaKe8LEhvucLgGYLTytuj4tPJ495F62hyNqPaxsUfYsLVsVLi//g84TgvKoqt6py"
    "xUU2rwoHwLuSF+qAa0tZqM11XwIf5xknnwMgXUbX6oBqy6RVl2o2RxeDFfKwRvr9N0QNLa"
    "UTooUMScYS++ab7KGdtSAHmZKJmIoYeLlQVNWxU3JSo5YdCuHZL1XQDu/xEerZ5QyeuYD9"
    "WEIqr8TmIzuvybZM+UeoyeaOAOWbPrkX6RdD6ftwGcZef1yCVUa89GXUyd+DMoXdHVMSM5"
    "moQA7zuapcCmPxf1XBF6eCBjCErSbql0S0Ur3Dvcdr+xyeEb16qlcle7+37h34ZHlU3dt/"
    "qCkQvcwzT7niBQ8Rr3L34uTOc0HHULDbyvVuL6TrY17billK8Qa1FG9QoXiD89zb9xCS1v"
    "Sjhmxc14RVYmCTjINhnciJOlfeoY0eVuKIjtO1FFf6ZKbDUQ2mw1EpU9H0G2frA1fXjpqt"
    "FaBY3xYl6rClMkejxOc1Rb+gFP0/UK9hQWYvpOMEUp9iRtTqqVqVrI1yX8TxrdEAYuj+Mg"
    "Ee5VDDe2RQ9I3rv7fzWdknKXFIBuSdwyf42cA6O+tZ2GNfThNrBUUxazFo2ws/oorgvZkq"
    "/2W5qjfzS0mBeMyk8iryApfNku/h08vuJ32SKrs="
)
