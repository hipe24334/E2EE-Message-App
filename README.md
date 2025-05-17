# MỤC TIÊU:
## Yêu cầu:
Xây dựng một ứng dụng nhắn tin cơ bản với các chức năng đăng nhập, xác thực trao đổi khóa an toàn và nhắn tin
tích hợp mã hóa đầu cuối.
Ứng dụng nhán tin được xây dựng dựa trên mô hình Client-Server, nơi mà Server quản lý các kết nối từ nhiều Client và nhận
nhiệm vụ chuyển tiếp thông điệp giữa chúng, ngoài ra Server cũng sẽ có nhiệm vụ hỗ trợ các Client trong quá trình xác
thực,… Còn Client sẽ có thể nhắn tin cho các Client khác mà đảm bảo tính bí mật, toàn vẹn của tin nhắn.
## Một số yêu cầu chính:
Mã hóa và giải mã thông điệp: Để đảm bảo tính bảo mật, các thông điệp phải được mã hóa trước khi gửi và giải
mã khi nhận. Thuật toán mã hóa được sử dụng là AES với chế độ CBC để đảm bảo tính toàn vẹn và bảo mật của
dữ liệu.3
Xử lý kết nối đồng thời: Các kết nối này được xử lý trong các "luồng" riêng biệt, đảm bảo rằng Server có thể tiếp
tục nhận và phản hồi các yêu cầu khác nhau mà không bị chậm trễ.
Giao thức truyền thông: TCP/IP được sử dụng làm giao thức truyền thông chính giữa Client và Server, đảm bảo
rằng dữ liệu được truyền một cách đáng tin cậy và theo thứ tự. TCP cũng hỗ trợ tái truyền và quản lý lưu lượng,
làm cho nó thích hợp cho ứng dụng yêu cầu truyền thông tin cậy như chat.
Giao thức xử lý tin nhắn: Tin nhắn được cấu trúc theo các định dạng được xác định trước, không chỉ bao gồm nội
dung tin nhắn đã được mã hoá mà còn cả metadata như tên người gửi, chữ ký,…
# MÔ TẢ:
## Các chức năng chính:
- Giao tiếp trực tiếp: Người dùng có thể gửi và nhận tin nhắn văn bản với nhau qua giao diện đơn giản và
thân thiện.
- Quản lý người dùng: Chương trình hỗ trợ quản lý người dùng, cho phép họ đăng nhập và tham gia trò
chuyện.
- Bảo mật: Dữ liệu được mã hóa và giải mã trước khi gửi và sau khi nhận, đảm bảo tính bảo mật trong quá
trình truyền thông.
- Tính linh hoạt: Chương trình hỗ trợ nhiều người dùng cùng lúc.
## Các thành phần chính:
- Client: Đại diện cho người dùng cuối, gửi và nhận tin nhắn từ server thông qua giao diện người dùng.
- Server: Quản lý kết nối từ các clients, xử lý tin nhắn và phân phối chúng đến các clients khác nếu cần.
- Giao thức truyền thông: Sử dụng giao thức TCP/IP để đảm bảo tính ổn định và toàn vẹn trong quá trình
truyền thông.
## Công nghệ và thuật toán:
- AES (Advanced Encryption Standard): Được sử dụng để mã hóa và giải mã dữ liệu, đảm bảo tính bảo mật
trong quá trình truyền thông.
- TCP (Transmission Control Protocol): Sử dụng làm giao thức truyền thông chính giữa Client và Server, đảm
bảo dữ liệu được truyền một cách đáng tin cậy và theo thứ tự.
- Diffie-Hellman: Sử dụng để tạo kênh truyền khóa an toàn đảm bảo bảo mật khi chia sẻ các khóa chung.
- Thủ tục xử lý tin nhắn: Các thông điệp được cấu trúc trong một định dạng cụ thể để dễ dàng phân tích và
xử lý.
