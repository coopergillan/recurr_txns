"""Unit tests for Transactions objects."""

from lib.transactions import Transaction
import pytest


@pytest.fixture
def raw_monthly_transaction():
    """A Python representation of the transactions from YAML."""
    return {
        "payee": "My employer",
        "txn_descr": "Pay estimate",
        "rrule": {
            "freq": "WEEKLY",
            "interval": 2,
            "byweekday": "FR",
        },
        "account": "Checking",
        "amount": "1000.00",
    }


def test_initializes_manually():
    transaction = Transaction(
        payee="Robert Hall",
        description="Accounting",
        frequency="weekly",
        interval=1,
        byweekday="FR",
        account="Checking",
        amount=-100,
    )
    assert transaction.payee == "Robert Hall"


def test_initializes_from_raw_input(raw_monthly_transaction):
    transaction = Transaction.from_raw(raw_monthly_transaction)
    assert transaction
