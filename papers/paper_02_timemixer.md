# Paper 02: TimeMixer

## Tên Bài Báo

TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting

## Vấn Đề Nghiên Cứu

Trình bày vấn đề dự báo chuỗi thời gian có nhiều thành phần xu hướng và mùa vụ ở các thang đo khác nhau.

## Ý Tưởng Chính

Tóm tắt ý tưởng phân rã và trộn thông tin đa thang đo để khai thác xu hướng, mùa vụ và biến động trong chuỗi thời gian.

## Mô Hình Đề Xuất

Mô tả ngắn gọn cách TimeMixer xử lý thông tin ở nhiều độ phân giải thời gian.

## Kết Quả Chính

Tóm tắt các kết quả thực nghiệm chính của bài báo.

## Điểm Mạnh

- Phù hợp với chuỗi thời gian có tính mùa vụ.
- Có khả năng khai thác thông tin ở nhiều thang đo.

## Hạn Chế

- Cần hiểu rõ quá trình phân rã chuỗi thời gian.
- Có thể khó triển khai đầy đủ trong phạm vi bài tập ngắn.

## Khả Năng Áp Dụng Cho Bài Toán Của Nhóm

Nhu cầu thuê xe đạp có tính chu kỳ theo giờ trong ngày, ngày trong tuần và mùa trong năm. Vì vậy, ý tưởng đa thang đo của TimeMixer phù hợp với việc tạo Fourier features, lag features và rolling features trong bài toán của nhóm.
