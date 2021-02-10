"""Unit tests for recurring transactions generator."""

from datetime import datetime

import pytest

from lib.recurr_txns import get_txn_rrule, show_txn_str


@pytest.fixture
def tab_map_dict():
    return {"Checking": 1, "Credit Card": 2}


@pytest.fixture
def txn_dict_base():
    return {
        "payee": "Martha Terry",
        "txn_descr": "Dog walking",
        "account": "Checking",
        "amount": 35.50,
    }


@pytest.fixture
def start_date():
    return datetime(2020, 12, 12, 23)


def test_it_gets_correct_rrule(start_date, txn_dict_base):
    rrule_info = {
        "freq": "WEEKLY",
        "interval": 1,
        "byweekday": "SA",
        "dtstart": start_date,
    }

    txn_dict = {**{"rrule": rrule_info}, **txn_dict_base}
    txn_rrule = get_txn_rrule(txn_dict, default_until=datetime(2020, 12, 31))

    # Check for correct count and details of the first transaction
    assert len(list(txn_rrule)) == 3
    assert txn_rrule[0] == datetime(2020, 12, 12, 23, 0)

    # Check that one is generated for each Saturday for rest of the month
    for next_txn, day_of_month in zip(txn_rrule, range(12, 31, 7)):
        assert next_txn.day == day_of_month


def test_it_shows_correct_string(txn_dict_base, start_date, tab_map_dict):
    txn_dict = {**{"dt": start_date}, **txn_dict_base}
    txn_string = show_txn_str(txn_dict, tab_map_dict)
    assert txn_string == ["12/12/2020", "Martha Terry; Dog walking", "", "$35.50"]
