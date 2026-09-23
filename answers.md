# Q1: Mỗi số 0 thêm vào nhân khối lượng tính toán kỳ vọng lên ≈ bao nhiêu lần? Vì sao?
≈ 16 lần. Vì mã băm sha256 trả về chuỗi hệ thập lục phân (hexadecimal: 16 ký tự từ 0-9, a-f). Xác suất để một ký tự bất kỳ rơi trúng số '0' là 1/16. Nên cứ thêm 1 số 0 ở đầu, độ khó lại nhân lên 16.

# Q2: Kiểm tra nonce tìm được tốn mấy lần gọi băm? Điều đó nói gì về PoW?
Kiểm tra chỉ tốn duy nhất 1 lần gọi hàm băm (băm ghép data + nonce và đếm số lượng số 0). Điều này thể hiện tính chất bất đối xứng (asymmetric) của PoW: Rất tốn thời gian để tìm ra đáp án, nhưng lại cực kỳ nhanh và dễ dàng để xác minh lại.

# Q3: Với n = 1,000,000 giao dịch, một proof chứa bao nhiêu giá trị băm?
Một proof chứa 20 giá trị băm. Cụ thể là số nguyên trần của log2(1.000.000) = 20.

# Q4: Nêu một hệ thống thực dùng đúng cơ chế này.
Hệ thống SPV (Simplified Payment Verification) của các "ví nhẹ" (light nodes) trên Bitcoin. Ví nhẹ không cần lưu toàn bộ khối, chỉ cần lưu phần đầu khối (Block Header) chứa Merkle root và yêu cầu một Merkle proof từ Full Node để xác minh nhanh 1 giao dịch có nằm trong khối hay không. (Cơ chế này cũng được dùng trong việc xác minh Airdrop claim trên Ethereum).