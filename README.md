# .dat Wallet Checker

This software is a **.dat wallet checker**.

## Features

- Verifies that the `.dat` file is readable and not corrupted.
- Extracts all addresses contained in the file.
- Compares the extracted addresses against a CSV file to check for balances.

## Usage

1. Provide a valid `.dat` wallet file.
2. Provide a CSV file containing address and balance information.
3. Run the script to check which addresses from the `.dat` file have a balance.

## Requirements

To set up the environment and install the necessary dependencies, follow these steps:

```bash
sudo apt install -y python3 python3-pip
sudo apt install libdb-dev libdb++-dev python3-dev build-essential
pip install bsddb3
git clone https://github.com/openwall/john.git
Download address balance Database (https://privatekey2bitcoin.com/freewallets/utxo.csv)


