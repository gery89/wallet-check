import re
import binascii
import hashlib
import os
from bsddb3 import db  # Make sure bsddb3 is installed: pip install bsddb3

# Base58 alphabet
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_decode(s):
    num = 0
    for char in s:
        num *= 58
        if char not in BASE58_ALPHABET:
            return None
        num += BASE58_ALPHABET.index(char)
    return num.to_bytes(25, byteorder='big')

def is_valid_bitcoin_address(address):
    try:
        decoded = base58_decode(address)
        if not decoded or len(decoded) != 25:
            return False
        checksum = decoded[-4:]
        hash1 = hashlib.sha256(decoded[:-4]).digest()
        hash2 = hashlib.sha256(hash1).digest()
        return checksum == hash2[:4]
    except Exception:
        return False

def is_base58_address(address):
    return (25 <= len(address) <= 35 and all(c in BASE58_ALPHABET for c in address))

def is_valid_berkeley_wallet(path):
    try:
        env = db.DBEnv()
        env.open('.', db.DB_CREATE | db.DB_INIT_MPOOL)
        wallet_db = db.DB(env)
        wallet_db.open(path, 'main', db.DB_BTREE, db.DB_RDONLY)
        cursor = wallet_db.cursor()
        key, value = cursor.first()
        cursor.close()
        wallet_db.close()
        env.close()
        return True
    except Exception:
        return False

# Load addresses and balances
address_file = 'utxo.csv'
address_balances = {}
with open(address_file, 'r') as file:
    for line in file:
        if ',' in line:
            address, balance = line.strip().split(',')
            address_balances[address.strip()] = balance.strip()

# Scan .dat files in current directory
folder = '.'
dat_files = [f for f in os.listdir(folder) if f.endswith('.dat')]

for filename in dat_files:
    path = os.path.join(folder, filename)
    print(f"\n📂 Checking file: {filename}")
    verified = True

    try:
        size = os.path.getsize(path)
        if size < 1024:
            print(f"⚠️  File size too small ({size} bytes).")
            verified = False

        if is_valid_berkeley_wallet(path):
            print("✅ File is a valid Berkeley DB wallet.")
        else:
            print("❌ File is NOT a valid Berkeley DB wallet (possibly corrupted).")
            verified = False

        with open(path, 'rb') as f:
            binary_data = f.read()

        try:
            text = binary_data.decode('utf-8', errors='ignore')
            if len(text.strip()) == 0:
                print("⚠️  File has no readable text.")
                verified = False
        except UnicodeDecodeError:
            print("❌ Failed to decode file content.")
            verified = False

        if verified:
            print("✅ File passed all checks.")
        else:
            print("❌ File failed verification.")

        # Search for valid addresses
        potential_addresses = re.findall(r'1[a-km-zA-HJ-NP-Z1-9]{25,34}', text)
        valid_addresses = []
        for addr in potential_addresses:
            if is_base58_address(addr) and is_valid_bitcoin_address(addr):
                balance = address_balances.get(addr)
                if balance:
                    valid_addresses.append((addr, balance))

        if valid_addresses:
            print("💰 Valid addresses with balance found:")
            for addr, balance in valid_addresses:
                print(f"   Address: {addr} | Balance: {balance}")
        else:
            print("ℹ️  No valid addresses with balance found.")

    except Exception as e:
        print(f"❌ Error while processing file: {e}")
        print("❌ File failed verification.")
