"""
Recurring Transactions Generator
"""

from datetime import datetime
from operator import itemgetter
from ruamel.yaml import YAML
import sys

from dateutil.rrule import rrule, MONTHLY, WEEKLY, YEARLY, SU, MO, TU, WE, TH, FR, SA
import pandas as pd

FREQ_MAP = {
    "MONTHLY": MONTHLY,
    "WEEKLY": WEEKLY,
    "YEARLY": YEARLY,
    "SU": SU,
    "MO": MO,
    "TU": TU,
    "WE": WE,
    "TH": TH,
    "FR": FR,
    "SA": SA,
}


def get_txn_rrule(txn_dict, default_until=None):
    """Given transaction dictionary, return recurring rule."""
    txn_rrule_raw = txn_dict["rrule"]
    txn_rrule_raw["freq"] = FREQ_MAP[txn_rrule_raw["freq"]]
    txn_rrule_raw["until"] = datetime.combine(
        txn_rrule_raw.get("until", default_until), datetime.min.time()
    )
    txn_rrule_raw["byweekday"] = FREQ_MAP.get(txn_rrule_raw.get("byweekday"))
    return rrule(**txn_rrule_raw)


def get_recurr_txns(yaml_config):
    """Read raw YAML config and get non-paused recurring transactions."""
    return [
        txn for txn in yaml_config["recurr_txns"] if txn.get("pause", False) is False
    ]


def show_txn_str(txn_dict, tab_map_dict):
    """Show transaction formatted for spreadsheet use."""

    txn_stg = [
        txn_dict["dt"].strftime("%m/%d/%Y"),
        "{payee}; {txn_descr}".format(**txn_dict),
    ]

    # Add an empty column for each tab required
    # This puts amounts for different accounts in different columns
    for i in range(tab_map_dict[txn_dict["account"]]):
        txn_stg.append("")
    txn_stg.append("${amount:.2f}".format(**txn_dict))
    return txn_stg


def main(yaml_config_file, output_to_file):
    """Get all recurring transactions and show them formatted properly."""
    with open(yaml_config_file) as yaml_file:
        raw_config = YAML(typ="safe").load(yaml_file)

    recurr_txns = get_recurr_txns(raw_config)
    default_until = datetime.combine(
        raw_config.get("DEFAULT_UNTIL", datetime.today().replace(month=12, day=31)),
        datetime.min.time(),
    )

    all_txns = []
    for recurr_txn in recurr_txns:

        # Get each of the dates that the transaction will occur
        these_txn_dts = get_txn_rrule(recurr_txn, default_until=default_until)

        # Add optional sort priority for transactions sharing same date
        recurr_txn["sort_priority"] = recurr_txn.get("sort_priority", 99)

        # Create a dictionary for each of these transactions and add it to all the others
        for this_txn_dt in these_txn_dts:

            # Set transaction values that don't change for each occurrence
            txn_constants = ["payee", "txn_descr", "amount", "account", "sort_priority"]
            this_txn = {key: recurr_txn[key] for key in txn_constants}

            # Add the next datetime to the rest of the transaction, then all transactions
            this_txn.update({"dt": this_txn_dt})
            all_txns.append(this_txn)

            # Reset the transaction dictionary
            this_txn = {}

    # Now sort all of the transactions
    sort_keys = ("dt", "sort_priority", "amount")
    sorted_txns_dict = sorted(all_txns, key=itemgetter(*sort_keys))

    tab_map_dict = raw_config["TAB_MAP"]

    sorted_txn_strs = [show_txn_str(txn, tab_map_dict) for txn in sorted_txns_dict]
    for txn in sorted_txn_strs:
        print(txn)

    # If indicated, send the sorted transaction strings to a file
    if output_to_file:
        df = pd.DataFrame(sorted_txn_strs)
        df.to_csv("results/mysortedtxns.csv", sep="\t", index=False, header=False)

    return sorted_txn_strs


if __name__ == "__main__":
    yaml_file = sys.argv[1]
    output_to_file = True
    main(yaml_file, output_to_file)
