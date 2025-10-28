import pandas as pd

from app.infrastructure.logger import logger


def debug_dataframe(df: pd.DataFrame, columns_to_show: list = []):
    """
    Debug the dataframe
    """

    logger.info("df Columns:")
    logger.info(df.columns)
    # logger.info("df head:")
    # logger.info(df.head())

    if columns_to_show:
        logger.info("df columns to show:")
        logger.info(df[columns_to_show].head())
