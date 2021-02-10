# recurr_txns

Generate recurring transactions in a spreadsheet-friendly format

## Getting started

* Run `script/bootstrap` to install the `pipenv` environment
* Run `script/setup` to create required directory

## Sample transactions

Add transactions to a YAML under the `recurr_txns` key. There are examples in
`input/sample_txns.yaml` like this:

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

* Run locally after running setup steps above:

```zsh
pipenv run python lib/recurr_txns.py input/sample_txns.yaml

['02/12/2021', 'John Doe; Childcare', '', '', '$-100.00']
['02/12/2021', 'My employer; Pay estimate', '', '', '$1000.00']
['02/14/2021', 'State Farm; Insurance payment', '', '', '$-75.00']
['02/19/2021', 'John Doe; Childcare', '', '', '$-100.00']
['02/26/2021', 'John Doe; Childcare', '', '', '$-100.00']
['02/26/2021', 'My employer; Pay estimate', '', '', '$1000.00']

[ ... ]
```

* Alternatively, run with Docker via `Makefile`. The transactions file **must be** placed in the `input/` directory:

```bash
make run INPUT_FILE=input/your_txns.yaml
```

## Building it

```bash
make build  # Builds the Docker image
```
