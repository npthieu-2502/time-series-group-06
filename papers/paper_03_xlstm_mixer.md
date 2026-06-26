# Paper 03: xLSTM-Mixer

## 1. Thông Tin Bài Báo

**Tên bài báo:** xLSTM-Mixer: Multivariate Time Series Forecasting by Mixing via Scalar Memories  
**Tác giả:** Maurice Kraus, Felix Divo, Devendra Singh Dhami và Kristian Kersting  
**Năm công bố:** 2024  
**Nguồn:** https://arxiv.org/abs/2410.16928  
**Lĩnh vực:** Dự báo chuỗi thời gian nhiều chiều, mô hình tuần tự và deep learning

## 2. Vấn Đề Nghiên Cứu

Trong dự báo chuỗi thời gian nhiều chiều, mô hình cần học đồng thời hai loại quan hệ:

1. Quan hệ theo thời gian của từng biến, ví dụ nhu cầu thuê xe ở giờ hiện tại phụ thuộc vào các giờ trước đó.
2. Quan hệ giữa các biến, ví dụ nhiệt độ, độ ẩm, thời tiết và giờ trong ngày cùng tác động đến nhu cầu thuê xe.

Nhiều mô hình chỉ tập trung mạnh vào một trong hai chiều trên hoặc cần kiến trúc attention tương đối tốn bộ nhớ. Bài báo đặt mục tiêu xây dựng một mô hình vừa học được động lực theo thời gian, vừa trộn được thông tin giữa các biến và vẫn sử dụng bộ nhớ hiệu quả.

## 3. Ý Tưởng Chính

xLSTM-Mixer kết hợp kiến trúc mixing với các khối xLSTM sử dụng scalar memories. Mô hình không tạo dự báo hoàn toàn từ đầu bằng một mạng sâu. Thay vào đó, nó bắt đầu bằng một dự báo tuyến tính được chia sẻ giữa các biến, sau đó sử dụng các khối xLSTM để tinh chỉnh dự báo này.

Mô hình xem dữ liệu từ nhiều góc nhìn:

- Góc nhìn theo thời gian để nắm bắt diễn biến và phụ thuộc tuần tự.
- Góc nhìn kết hợp thời gian và biến để học tương tác trong dữ liệu nhiều chiều.

Cuối cùng, hai góc nhìn được hòa giải để tạo ra dự báo cuối. Cách thiết kế này tận dụng sự ổn định của mô hình tuyến tính và khả năng học động lực phức tạp của xLSTM.

## 4. Mô Hình Đề Xuất

Quy trình tổng quát của xLSTM-Mixer gồm:

1. **Đầu vào nhiều chiều:** nhận một cửa sổ lịch sử có nhiều bước thời gian và nhiều biến.
2. **Linear forecast:** tạo dự báo tuyến tính ban đầu với tham số được chia sẻ giữa các biến.
3. **Temporal mixing:** xử lý thông tin tuần tự để học mẫu lặp, xu hướng và phụ thuộc dài hạn.
4. **Time-variate mixing:** trộn thông tin giữa chiều thời gian và chiều biến để học các tương tác đa biến.
5. **xLSTM refinement:** sử dụng các khối xLSTM làm thành phần chính để tinh chỉnh dự báo tuyến tính.
6. **Reconciliation:** kết hợp hai góc nhìn thành kết quả dự báo cuối cùng.

Điểm đáng chú ý là mô hình vẫn giữ tinh thần của mạng hồi quy nhưng được tổ chức theo kiến trúc mixing. Đây là một hướng kết hợp giữa recurrent model và mixer architecture.

## 5. Kết Quả Chính

Theo kết quả được các tác giả báo cáo:

- xLSTM-Mixer đạt hiệu năng tốt trong các bài toán dự báo dài hạn trên nhiều benchmark chuỗi thời gian.
- Mô hình có kết quả cạnh tranh hoặc tốt hơn nhiều phương pháp hiện đại được dùng làm đối chứng.
- Mô hình sử dụng ít bộ nhớ so với nhiều kiến trúc phức tạp khác.
- Các phân tích thành phần cho thấy dự báo tuyến tính, khối xLSTM và việc kết hợp nhiều góc nhìn đều đóng vai trò quan trọng.

Nhóm không trích một con số duy nhất vì kết quả thay đổi theo dataset và forecast horizon. Khi viết báo cáo cuối, các bảng kết quả cụ thể cần được đối chiếu trực tiếp với phiên bản bài báo được nhóm sử dụng.

## 6. Điểm Mạnh

- Học được cả quan hệ theo thời gian và quan hệ giữa các biến.
- Kết hợp được ưu điểm của dự báo tuyến tính và mạng tuần tự sâu.
- Phù hợp với bài toán chuỗi thời gian nhiều chiều.
- Có khả năng mô hình hóa phụ thuộc dài hạn.
- Theo báo cáo của tác giả, mô hình có hiệu quả sử dụng bộ nhớ tốt.
- Kiến trúc cung cấp một hướng thay thế cho các mô hình Transformer dựa nhiều vào attention.

## 7. Hạn Chế

- Kiến trúc xLSTM-Mixer phức tạp hơn GRU hoặc LSTM cơ bản, khó triển khai đầy đủ trong thời gian ngắn.
- Hiệu quả phụ thuộc vào cách chọn input window, forecast horizon và siêu tham số.
- Kết quả trên benchmark dự báo dài hạn chưa đảm bảo mô hình sẽ tốt nhất trên dữ liệu Bike Sharing.
- Dataset của nhóm có nhiều biến thời gian dạng phân loại nên vẫn cần feature engineering phù hợp trước khi đưa vào mô hình.
- Việc tái lập chính xác kết quả bài báo cần code chính thức, cấu hình thí nghiệm và tài nguyên tính toán phù hợp.

## 8. Khả Năng Áp Dụng Cho Bài Toán Của Nhóm

Bài toán của nhóm có đầu vào nhiều chiều gồm thời gian, mùa vụ, thời tiết, nhiệt độ, độ ẩm, tốc độ gió và nhu cầu thuê xe trong quá khứ. Đầu ra là biến `cnt` tại giờ tiếp theo. Vì vậy, bài toán cần học cả chu kỳ theo thời gian lẫn ảnh hưởng giữa các biến, tương đồng với động lực nghiên cứu của xLSTM-Mixer.

Trong phạm vi bài tập, nhóm chưa triển khai nguyên bản xLSTM-Mixer vì kiến trúc tương đối phức tạp. Thay vào đó, nhóm áp dụng các bài học sau:

- Dùng input window 24 giờ để giữ thông tin tuần tự.
- Đưa nhiều biến thời gian và thời tiết vào cùng mô hình.
- Sử dụng lag features và Fourier features để biểu diễn mùa vụ.
- Chọn GRU làm mô hình nâng cao khả thi, sau đó so sánh với baseline tuyến tính và Random Forest.

GRU không thay thế hoàn toàn xLSTM-Mixer, nhưng là bước thực nghiệm phù hợp để nhóm kiểm chứng giá trị của mô hình tuần tự trên dataset Bike Sharing.

## 9. Kết Luận

xLSTM-Mixer là một hướng tiếp cận mới kết hợp dự báo tuyến tính, mixing và xLSTM để xử lý chuỗi thời gian nhiều chiều. Bài báo có liên hệ trực tiếp với đề tài nhóm vì cùng yêu cầu học quan hệ theo thời gian và giữa các biến. Ý tưởng của bài báo cung cấp cơ sở lý thuyết cho việc lựa chọn input window nhiều chiều và mô hình GRU trong phần thực nghiệm.
