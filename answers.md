# Q1: Mỗi số 0 thêm vào nhân khối lượng tính toán kỳ vọng lên ≈ bao nhiêu lần? Vì sao?
≈ 16 lần. Vì mã băm sha256 trả về chuỗi hệ thập lục phân (hexadecimal: 16 ký tự từ 0-9, a-f). Xác suất để một ký tự bất kỳ rơi trúng số '0' là 1/16. Nên cứ thêm 1 số 0 ở đầu, độ khó lại nhân lên 16.

# Q2: Kiểm tra nonce tìm được tốn mấy lần gọi băm? Điều đó nói gì về PoW?
Kiểm tra chỉ tốn duy nhất 1 lần gọi hàm băm (băm ghép data + nonce và đếm số lượng số 0). Điều này thể hiện tính chất bất đối xứng (asymmetric) của PoW: Rất tốn thời gian để tìm ra đáp án, nhưng lại cực kỳ nhanh và dễ dàng để xác minh lại.

# Q3: Với n = 1,000,000 giao dịch, một proof chứa bao nhiêu giá trị băm?
Một proof chứa 20 giá trị băm. Cụ thể là số nguyên trần của log2(1.000.000) = 20.

# Q4: Nêu một hệ thống thực dùng đúng cơ chế này.
Hệ thống SPV (Simplified Payment Verification) của các "ví nhẹ" (light nodes) trên Bitcoin. Ví nhẹ không cần lưu toàn bộ khối, chỉ cần lưu phần đầu khối (Block Header) chứa Merkle root và yêu cầu một Merkle proof từ Full Node để xác minh nhanh 1 giao dịch có nằm trong khối hay không. (Cơ chế này cũng được dùng trong việc xác minh Airdrop claim trên Ethereum).

# Lab 3.3 Tasks

## Task 1: Chạy hai lần cùng thông điệp — chữ ký có giống nhau không? RFC nào giải thích điều này?
Nếu ký cùng một thông điệp bằng **cùng một khóa riêng (private key)**, chữ ký sinh ra sẽ **giống hệt nhau** 100%. 
Điều này được giải thích bởi tiêu chuẩn **RFC 6979**. Thay vì dùng một số ngẫu nhiên (nonce `k`) mỗi lần ký như ECDSA truyền thống, chuẩn này tạo ra `k` một cách tất định (deterministic) dựa trên chính thông điệp và khóa riêng, giúp tránh các lỗ hổng bảo mật do thuật toán tạo số ngẫu nhiên kém.

## Task 2: Giải thích vì sao khôi phục ra địa chỉ khác lại là bằng chứng toàn vẹn.
Bởi vì chữ ký số mã hóa mối liên hệ toán học giữa nội dung thông điệp gốc và khóa riêng của người gửi. Khi thông điệp bị sửa đổi (dù chỉ 1 ký tự), mã băm của nó thay đổi hoàn toàn (hiệu ứng tuyết lở). Hàm `recover_message` kết hợp mã băm sai này với chữ ký gốc sẽ tính ngược ra một địa chỉ (public key) hoàn toàn rác/khác biệt. Người nhận thấy địa chỉ khôi phục không khớp với địa chỉ người gửi ban đầu sẽ lập tức biết nội dung đã bị thay đổi trên đường truyền (đảm bảo tính toàn vẹn).