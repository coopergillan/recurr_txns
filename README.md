# recurr_txns

Generate recurring transactions in a spreadsheet-friendly format

## Getting started

Run `script/bootstrap` to install the `pipenv` environment.

## Sample transactions

Add transactions to a YAML under the `recurr_txns` key. There are examples in
`sample_txns.yaml` like this:

```yaml
recurr_txns:
  - payee: John Doe
    txn_descr: Childcare
    rrule:
      freq: WEEKLY
      interval: 1
      byweekday: FR
    account: Checking
    amount: -100.00
```

## Running it

Use the following command to generate the transactions

```zsh
pipenv run python lib/recurr_txns.py sample_txns.yaml
```
