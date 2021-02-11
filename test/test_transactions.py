"""Unit tests for Transactions objects."""

from lib.transactions import Transaction


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


def test_initializes_from_yaml():
    transaction = Transaction.from_yaml("test_transactions.yaml")
    assert transaction
