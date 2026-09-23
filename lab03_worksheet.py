import hashlib
import time

# (a) Avalanche effect / Hiệu ứng tuyết lở
print("--- (a) Avalanche effect ---")
print(hashlib.sha256(b"Blockchain 2026").hexdigest())
print(hashlib.sha256(b"blockchain 2026").hexdigest())

# (b) Toy PoW: find nonce so that sha256(data+nonce) starts with k zeros
print("\n--- (b) Toy PoW ---")
def toy_pow(data, k):
    prefix = "0" * k
    nonce = 0
    start_time = time.time()
    
    while True:
        # Ghép data và nonce, sau đó chuyển sang dạng bytes để băm
        text = f"{data}{nonce}".encode('utf-8')
        hash_result = hashlib.sha256(text).hexdigest()
        
        # Kiểm tra xem mã băm có bắt đầu bằng k số 0 hay không
        if hash_result.startswith(prefix):
            end_time = time.time()
            return nonce, hash_result, end_time - start_time
        
        nonce += 1

data_string = "Blockchain 2026"
k_zeros = 4 # Bạn có thể đổi k = 5, 6 để thấy thời gian chạy lâu hơn

print(f"Đang tìm nonce cho data '{data_string}' với {k_zeros} số 0 ở đầu...")
nonce, final_hash, time_taken = toy_pow(data_string, k_zeros)

print(f"Nonce tìm được: {nonce}")
print(f"Mã băm: {final_hash}")
print(f"Thời gian chạy: {time_taken:.5f} giây")