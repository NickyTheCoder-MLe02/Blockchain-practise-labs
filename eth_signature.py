from eth_account import Account
from eth_account.messages import encode_defunct

# Tạo một tài khoản mới ngẫu nhiên
acct = Account.create() # TUYỆT ĐỐI không dùng khóa này cho tiền thật
print("address:", acct.address) 

msg = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 3")
sig = Account.sign_message(msg, acct.key)
print("r,s,v:", hex(sig.r), hex(sig.s), sig.v)

# Khôi phục địa chỉ chỉ từ chữ ký
who = Account.recover_message(msg, signature=sig.signature)
print("recovered:", who, "| match:", who == acct.address)

# Sửa 1 ký tự (tamper)
bad = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 4")
print("tampered ->", Account.recover_message(bad, signature=sig.signature))