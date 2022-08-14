"""
Clients for various finance tools
"""

from urllib.parse import urljoin

import requests
from requests.structures import CaseInsensitiveDict

from finance.data import Transaction


class FireflyClient:
    """
    Client for working with Firefly-III server.
    """

    def __init__(self, host: str, access_token: str, source_name: str):
        self.host = host
        self.access_token = access_token
        self.source_name = source_name


def put_transaction(client: FireflyClient, t: Transaction):
    """
    Upload provided transaction in firefly server
    """

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.api+json"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {client.access_token}"

    # HACK: We don't check for transaction duplication right now. I
    # also believe firefly-iii might not do this validation.
    res = requests.post(urljoin(client.host, "/api/v1/transactions"), data={
        "error_if_duplicate_hash": True,
        "apply_rules": True,
        "fire_webhooks": True,
        "group_title": "",
        "transactions": [{
            "type": "deposit" if t.is_deposit else "withdrawal",
            "date": t.value_date.isoformat(),
            "amount": None,
            "description": t.narration,
            "source_name": "HDFC Orderly Bazaar",
            "external_id": t.bank_reference
        }]
    }, headers=headers)

    return res.json()
