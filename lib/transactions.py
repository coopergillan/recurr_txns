"""Main Transaction object module."""


class Transaction(object):
    def __init__(
        self, payee, description, frequency, interval, byweekday, account, amount
    ):
        self.payee = payee
        self.description = description
        self.frequency = frequency
        self.interval = interval
        self.byweekday = byweekday
        self.account = account
        self.amount = amount

    @classmethod
    def from_raw(cls, input_raw):
        """Takes a dictionary matching the raw input expected from the YAML files."""
        matching_keys = ["payee", "account", "amount"]
        new_input = {k: input_raw[k] for k in matching_keys}

        # Manually put these together for now =|
        new_input["description"] = input_raw["txn_descr"]
        new_input["frequency"] = input_raw["rrule"]["freq"]
        new_input["interval"] = input_raw["rrule"]["interval"]
        new_input["byweekday"] = input_raw["rrule"]["byweekday"]
        return cls(**new_input)
