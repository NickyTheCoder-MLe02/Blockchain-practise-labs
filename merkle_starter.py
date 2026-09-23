#!/usr/bin/env python3
"""Lab 3.2 — Merkle tree (starter).
Hoàn thành 3 TODO rồi chạy: python3 merkle_starter.py
Mọi dòng CHECK phải in OK. All CHECK lines must print OK.
"""
import hashlib

def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def merkle_root(leaves: list[bytes]) -> bytes:
    """TODO 1: dựng cây từ dưới lên, trả về băm gốc."""
    if not leaves:
        return b""
    current_level = leaves.copy()
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            # Tầng lẻ: nhân đôi phần tử cuối
            right = current_level[i] if i + 1 == len(current_level) else current_level[i+1]
            next_level.append(H(left + right))
        current_level = next_level
    return current_level[0]

def merkle_proof(leaves: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    """TODO 2: trả về [(sibling_digest, sibling_is_left), ...] từ lá lên gốc."""
    proof = []
    current_level = leaves.copy()
    curr_idx = index
    
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i] if i + 1 == len(current_level) else current_level[i+1]
            
            if i == curr_idx or i + 1 == curr_idx:
                if curr_idx % 2 == 0:  # node hiện tại là node bên trái
                    sibling = right
                    sibling_is_left = False
                else:                  # node hiện tại là node bên phải
                    sibling = left
                    sibling_is_left = True
                proof.append((sibling, sibling_is_left))
            
            next_level.append(H(left + right))
            
        current_level = next_level
        curr_idx //= 2
        
    return proof

def verify_proof(leaf_hash: bytes, proof: list[tuple[bytes, bool]], root: bytes) -> bool:
    """TODO 3: tính ngược lên gốc rồi so sánh."""
    curr_hash = leaf_hash
    for sibling, sibling_is_left in proof:
        if sibling_is_left:
            curr_hash = H(sibling + curr_hash)
        else:
            curr_hash = H(curr_hash + sibling)
    return curr_hash == root

# ------------------------------------------------------------------ checks
if __name__ == "__main__":
    txs = [f"tx{i}: A->B {i} coin".encode() for i in range(8)]
    leaves = [H(t) for t in txs]
    root = merkle_root(leaves)
    print("root:", root.hex())

    # CHECK 1: proof đúng cho mọi lá
    ok = all(verify_proof(leaves[i], merkle_proof(leaves, i), root) for i in range(8))
    print("CHECK 1 (all 8 proofs valid):", "OK" if ok else "FAIL")

    # CHECK 2: proof có đúng log2(8)=3 phần tử
    print("CHECK 2 (proof length == 3):", "OK" if len(merkle_proof(leaves, 4)) == 3 else "FAIL")

    # CHECK 3: lá bị sửa phải trượt
    fake = H(b"tx4: A->B 999999 coin")
    print("CHECK 3 (tampered leaf fails):",
          "OK" if not verify_proof(fake, merkle_proof(leaves, 4), root) else "FAIL")

    # CHECK 4: số lá lẻ (7) vẫn chạy
    l7 = leaves[:7]
    r7 = merkle_root(l7)
    print("CHECK 4 (odd count works):",
          "OK" if all(verify_proof(l7[i], merkle_proof(l7, i), r7) for i in range(7)) else "FAIL")