import re
import binascii
import hashlib
import os
import subprocess
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

# Function to extract Bitcoin hash using bitcoin2john.py
def extract_bitcoin_hash(wallet_path, bitcoin2john_path):
    try:
        # Execute bitcoin2john.py using subprocess
        result = subprocess.run(
            ['python3', bitcoin2john_path, wallet_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Error running bitcoin2john: {result.stderr}")
            return None
        
        # Extract the hash from the output
        hash_line = result.stdout.strip()
        if hash_line:
            print(f"✅ Bitcoin Hash: {hash_line}")
            return hash_line
        else:
            print("❌ No hash found.")
            return None
    except Exception as e:
        print(f"❌ Error extracting Bitcoin hash: {e}")
        return None

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
        # Check file size (must be greater than 1024 bytes)
        size = os.path.getsize(path)
        if size < 1024:
            print(f"⚠️  File size too small ({size} bytes).")
            verified = False

        # Check if it is a valid Berkeley DB wallet
        if is_valid_berkeley_wallet(path):
            print("✅ File is a valid Berkeley DB wallet.")
        else:
            print("❌ File is NOT a valid Berkeley DB wallet (possibly corrupted).")
            verified = False

        # Check if the file is readable as UTF-8 text
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

        # If any verification fails, don't attempt to extract the Bitcoin hash
        if not verified:
            print("❌ File failed verification. Skipping Bitcoin hash extraction.")
        else:
            print("✅ File passed all checks.")
            # Extract Bitcoin hash only if the file passes all verifications
            bitcoin2john_path = 'john/run/bitcoin2john.py'  # Update this with the correct path if necessary
            bitcoin_hash = extract_bitcoin_hash(path, bitcoin2john_path)

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
