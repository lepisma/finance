"""
Module for parsing and working with data structures
"""

from typing import List
import pandas as pd
import numpy as np
import re
from dataclasses import dataclass
import datetime


@dataclass
class Transaction:
    """
    A simple transaction representation mostly driven by what I see in my bank
    account's dumps.
    """

    narration: str
    bank_reference: str
    date: datetime.date
    value_date: datetime.date
    amount: float
    is_deposit: bool = False


def parse_hdfc_format(xlsx_filepath: str) -> List:
    """
    Parse HDFC bank's XLSX format statements and return individual
    transactions in a list.
    """

    rows = pd.read_excel(xlsx_filepath).to_records()

    transactions = []

    for row in rows:
        try:
            if re.match(r"\d{2}/\d{2}/\d{2}", row[1]):
                # This is a row with transaction
                is_deposit = np.isnan(row[5])

                transactions.append(Transaction(
                    narration=row[2],
                    bank_reference=row[3],
                    date=datetime.datetime.strptime(row[1], "%d/%m/%y").date(),
                    value_date=datetime.datetime.strptime(row[4], "%d/%m/%y").date(),
                    amount=row[6] if is_deposit else row[5],
                    is_deposit=is_deposit
                ))

        except TypeError:
            # There will be cases where this value will be nan, we just want to
            # ignore those rows
            continue

    return transactions
