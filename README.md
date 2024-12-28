# Hệ thống cào dữ liệu từ Facebook (group hoặc fanpage)
> Group 09
> 
> Lớp học phần: (ELC3009_1)
> 
> Giáo viên: Nguyễn Thành Thủy
> 
## Sử dụng heroku
### Bước 1: Tạo clone của github này https://github.com/ifindnemo/toolScrapingFB, kết nối với heroku, bật auto deploy trên heroku để tự động deploy khi push file lên github.
### Bước 2: Tạo 1 cluster trên MongoDB, tạo 1 database mới trong cluster đó (Xài cluster loại M0-free cũng ổn).
- Database access thêm một user với role *Read and write any database*. Network access thêm địa chỉ ip để có thể truy cập từ bất cứ đâu, hoặc ip cụ thể bạn muốn.
### Bước 3: Cài đủ buildpack trên heroku, bao gồm:
- buildpack python có sẵn
- https://github.com/heroku/heroku-buildpack-chrome-for-testing
#### Thiết lập các Config Vars bao gồm: MONGODB, PASSWORD_SECRET. Còn REDISCLOUD_URL sẽ tự tạo khi thêm add-on Redis Cloud vào app trên heroku.
#### Về web dyno và worker dyno thì nên dùng Standard-2X (8 CPU, 1GB RAM)
### Bước 4: Thiết lập một website, ví dụ source code: https://www.yumyum.social/crawl.html, cần 2 function test() và sendrequest như script trong html này.
### Bước 5: Chạy thui :3
## Chạy trên local: (sẽ up lên trong tương lai gần, hiện tại tui sắp ngất rồi)
### Bước 1:??
### Bước 2:??
### Bước 3:??
- User có thể nhập loại group/fanpage, URL, số lượng bài đăng.
- Website đang sử dụng để cào: https://www.yumyum.social/crawl.html
![pic1](https://github.com/user-attachments/assets/74eab2b8-b27c-4065-8621-c4ba549ea6dd)

- Ví dụ thao tác fetch trên website:
`fetch("https://<heroku app name secret>.herokuapp.com/crawl", {
                        method: "POST",
                        body: formData
                    })`
> Thay đường dẫn thành localhost nếu chạy trên local.
> 
> Thay các biến trong server.py và celeryapp.py ngay trong code, còn hiện tại file code đang lấy các biến từ Enviroment variables của Heroku.
- Vì sử dụng heroku và dyno Standard-2X nên sẽ tốn tiền, 1 dyno S-2X là 0.069$/1h. Hiện tại code cũng sử dụng add-on Redis Cloud trên heroku
- Sử dụng web dyno chạy server.py để xử lý các request https từ Website. Còn worker dyno với celery để chạy celeryapp.py, xử lý không đồng bộ để cào dữ liệu (chạy trên background, vì việc cào sẽ hơn 30s. Heroku giới hạn thời gian phản hồi tối đa là 30s, không tăng thêm được.
- Việc sư dụng celery sẽ giúp tránh việc "Connection timed out" khi thời gian phản hồi quá 30s.

- Sau khi cào sẽ lưu kết quả vào MongoDB và trả về kết quả trên Website:
![pic2](https://github.com/user-attachments/assets/e8e9cf8f-e5ac-48a9-8d27-828a25a863fd)


# Ghi chú thêm:
### Celery:
- Celery là một hệ thống xử lý hàng đợi công việc phân tán (distributed task queue) được sử dụng để xử lý các tác vụ không đồng bộ (asynchronous tasks). Nó cho phép bạn chạy các tác vụ tốn thời gian (như gửi email, xử lý dữ liệu lớn, hoặc gọi API) ở chế độ nền (background), giúp ứng dụng chính không bị chậm hoặc gián đoạn.
- Đặc điểm chính của Celery:
> Xử lý không đồng bộ: Celery cho phép thực hiện các tác vụ song song hoặc ở chế độ nền.
> 
> Phân tán: Có thể chạy trên nhiều máy chủ để tăng hiệu suất.
> 
> Hỗ trợ nhiều message broker: Celery sử dụng các message broker như Redis, RabbitMQ, hoặc Amazon SQS để giao tiếp giữa các thành phần.
> 
> Lập lịch công việc (Task Scheduling): Celery hỗ trợ việc lập lịch các công việc định kỳ, giống như cron.
- Cách hoạt động của Celery:
> Ứng dụng chính gửi một tác vụ vào hàng đợi thông qua broker.
> 
> Worker (là các tiến trình Celery) nhận tác vụ từ hàng đợi và xử lý nó.
> 
> Sau khi hoàn thành, worker có thể lưu kết quả vào một backend (Redis, database, hoặc một file system).
### Redis:
- Redis (Remote Dictionary Server) là một cơ sở dữ liệu NoSQL lưu trữ dữ liệu dưới dạng key-value trong bộ nhớ RAM, giúp cho việc đọc/ghi dữ liệu cực kỳ nhanh chóng.
- Tính năng chính của Redis:
> Tốc độ cao: Dữ liệu được lưu trữ trong RAM, do đó các thao tác đọc/ghi diễn ra rất nhanh.
> 
> Hỗ trợ nhiều kiểu dữ liệu: Redis không chỉ hỗ trợ key-value, mà còn hỗ trợ danh sách (lists), tập hợp (sets), bản đồ (hashes), và hơn thế nữa.
> 
> Hỗ trợ Pub/Sub: Redis có thể được sử dụng làm hệ thống nhắn tin (message broker) bằng cách sử dụng tính năng xuất bản/đăng ký (publish/subscribe).
> 
> Persistence (lưu trữ bền vững): Redis có thể ghi dữ liệu từ RAM xuống đĩa để đảm bảo dữ liệu không bị mất sau khi khởi động lại.
- Vai trò của Redis trong Celery: Redis thường được sử dụng như một message broker trong Celery. Khi Celery gửi tác vụ, nó sẽ được lưu trữ trong hàng đợi Redis, sau đó worker sẽ lấy tác vụ từ đó để xử lý.


