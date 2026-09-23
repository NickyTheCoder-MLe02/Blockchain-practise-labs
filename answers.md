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

# Lab 04 Tasks

## Task 4.1
**Q1: Target có khoảng bao nhiêu chữ số hex 0 dẫn đầu? Một header hợp lệ đại diện cho ~2^? phép băm?**
Target của block 840,000 bắt đầu bằng khoảng 21 chữ số hex `0` (do có khoảng 84 bit 0 dẫn đầu, 84/4 = 21). 
Vì SHA-256 trả về 256 bits và ta cần khoảng 84 bits đầu tiên bằng 0, độ khó tìm ra chuỗi hash thỏa mãn xấp xỉ 2^84. Vậy một block hợp lệ đại diện cho khoảng ~2^84 phép thử băm (hashes).

**Q2: Kiểm PoW chỉ tốn 2 lần băm; tìm ra nó tốn cả mạng ~10 phút. Tính chất nào của SHA-256 tạo ra bất đối xứng này?**
Tính chất **"kháng tiền ảnh" (Pre-image resistance)** và **"bất khả đoán" (Unpredictability/One-way)**. Ta không thể suy ngược từ mã băm đầu ra (target) để tìm input (nonce), và cũng không có thuật toán nào nhanh hơn việc "thử sai" (Brute-force) liên tục. Tuy nhiên hàm tính băm lại có tốc độ cực nhanh, nên việc tính lại 1 lần để xác minh kết quả là ngay lập tức.

## Task 4.2
**Q3: Giao dịch trả ~3.6 triệu sat/vB. Nhìn ngày tháng: chuyện gì đang diễn ra, và nó dạy gì về cách phí hình thành?**
Block 840,000 xảy ra vào ngày 20/04/2024, đúng ngày diễn ra sự kiện **Bitcoin Halving lần thứ 4**, trùng với việc ra mắt giao thức **Runes** trên Bitcoin. Việc hype đổ xô mint token Runes trong block lịch sử tạo ra sự cạnh tranh khốc liệt. Mức phí (Fee) ở Bitcoin không bị áp đặt cố định mà được hình thành qua cơ chế **Mempool Auction (đấu giá không gian block)** — người dùng muốn giao dịch được đưa vào block ưu tiên sẽ phải chủ động đẩy mức fee/vB lên cao hơn đối thủ.

**Q4: Tổng output coinbase là 4,075,061,499 sat; trợ cấp là 312,500,000 sat (3.125 BTC). Phần chênh từ đâu ra?**
Phần chênh lệch khổng lồ (khoảng ~37.62 BTC) đến từ **tổng phí giao dịch (Transaction Fees)** của toàn bộ 3,049 giao dịch thường trong block cộng lại. Output của giao dịch Coinbase (phần thưởng thợ đào) luôn bằng: Khối lượng trợ cấp cố định (Block Subsidy) + Tổng phí giao dịch của block đó.

## Task 4.3
**Q5: Root tính được khớp header. Giải thích trong 2–3 câu điều đó chứng minh gì về danh sách giao dịch của block, nêu rõ tính chất băm liên quan.**
Điều này chứng minh danh sách 3050 giao dịch mà ta tải về từ API hoàn toàn khớp, không bị sửa đổi, thiếu hoặc dư so với nguyên bản lúc block được thợ đào tạo ra. Tính chất băm liên quan là **Hiệu ứng tuyết lở (Avalanche Effect) và tính kháng va chạm (Collision resistance)** — chỉ cần 1 bit hoặc 1 giao dịch trong số 3050 tx bị sai lệch, Merkle Root tính ra sẽ thay đổi hoàn toàn và không thể khớp với header.