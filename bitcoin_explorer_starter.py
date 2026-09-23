#!/usr/bin/env python3
"""Lab 04 — Real Bitcoin Blocks: PoW, Fees & Merkle Root"""

import hashlib
import json
import urllib.request
import urllib.error
import sys
import math

# Block 840,000: The 4th halving block
PINNED_HEIGHT = 840000
API_BASE = "https://blockstream.info/api"

def dsha256(b: bytes) -> bytes:
    """Double SHA-256: H(H(b))."""
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def get_json(url: str) -> dict | list:
    """Helper to fetch and parse JSON from the API."""
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        sys.exit(1)

def get_block_hash(height: int) -> str:
    url = f"{API_BASE}/block-height/{height}"
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching block hash: {e}")
        sys.exit(1)

def get_block_header(block_hash: str) -> bytes:
    url = f"{API_BASE}/block/{block_hash}/header"
    try:
        with urllib.request.urlopen(url) as response:
            return bytes.fromhex(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching header: {e}")
        sys.exit(1)

def get_txs(block_hash: str) -> list[str]:
    url = f"{API_BASE}/block/{block_hash}/txids"
    return get_json(url)

def get_tx(txid: str) -> dict:
    url = f"{API_BASE}/tx/{txid}"
    return get_json(url)

# ==================== IMPLEMENTATIONS ====================

def bits_to_target(bits: int) -> int:
    """TODO 1: bits = 0xEEMMMMMM -> target = MMMMMM * 256^(EE - 3)"""
    bits_hex = f"{bits:08x}"
    exponent = int(bits_hex[:2], 16)
    mantissa = int(bits_hex[2:], 16)
    target = mantissa * (256 ** (exponent - 3))
    return target

def compute_fee_rate(tx: dict) -> float:
    """TODO 2: compute fee rate in sat/vB.
    fee = sum(inputs) - sum(outputs)
    vsize = ceil(weight / 4)
    """
    total_in = sum(vin["prevout"]["value"] for vin in tx["vin"] if "prevout" in vin)
    total_out = sum(vout["value"] for vout in tx["vout"])
    fee = total_in - total_out
    
    vsize = math.ceil(tx["weight"] / 4)
    return fee / vsize

def compute_merkle_root(txids: list[str]) -> str:
    """TODO 3: fold the block's txids into the Merkle root.
    - double SHA-256 (dsha256)
    - byte-reverse txids before hashing, reverse again at the end
    - Odd level -> duplicate the last node
    """
    if not txids:
        return ""
        
    current_level = [bytes.fromhex(txid)[::-1] for txid in txids]
    
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i] if i + 1 == len(current_level) else current_level[i+1]
            next_level.append(dsha256(left + right))
        current_level = next_level
        
    root_bytes = current_level[0]
    return root_bytes[::-1].hex()

# ==================== MAIN CHECKS ====================

if __name__ == "__main__":
    print(f"--- Fetching Block {PINNED_HEIGHT} ---")
    block_hash = get_block_hash(PINNED_HEIGHT)
    print(f"Block hash: {block_hash}")

    block_info = get_json(f"{API_BASE}/block/{block_hash}")
    
    # 1. PoW CHECK
    print("\n--- Task 4.1: PoW ---")
    header_bytes = get_block_header(block_hash)
    computed_hash = dsha256(header_bytes)[::-1].hex()
    print("CHECK (Header dSHA256 matches Block ID):", "OK" if computed_hash == block_hash else "FAIL")
    
    bits = block_info["bits"]
    target = bits_to_target(bits)
    block_hash_int = int(block_hash, 16)
    
    print(f"Bits  : 0x{bits:08x}")
    print(f"Target: {target:064x}")
    print(f"Hash  : {block_hash_int:064x}")
    print("CHECK (Hash < Target):", "OK" if block_hash_int < target else "FAIL")

    # 2. FEE CHECK
    print("\n--- Task 4.2: Fee Rate ---")
    txids = get_txs(block_hash)
    print(f"Block contains {len(txids)} transactions.")
    
    # txids[0] is coinbase, txids[1] is the first normal tx
    first_normal_tx = get_tx(txids[1])
    fee_rate = compute_fee_rate(first_normal_tx)
    print(f"Tx {txids[1][:8]}... fee rate: {fee_rate:.2f} sat/vB")
    print("CHECK (Fee rate > 3000 sat/vB for Halving Runes hype):", "OK" if fee_rate > 3000 else "FAIL")

    # 3. MERKLE ROOT CHECK
    print("\n--- Task 4.3: Merkle Root ---")
    computed_root = compute_merkle_root(txids)
    expected_root = block_info["merkle_root"]
    print(f"Expected: {expected_root}")
    print(f"Computed: {computed_root}")
    print("CHECK (Merkle Root matches):", "OK" if computed_root == expected_root else "FAIL")