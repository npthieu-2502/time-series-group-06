# Paper 01: iTransformer

## Tên Bài Báo

iTransformer: Inverted Transformers Are Effective for Time Series Forecasting

## Vấn Đề Nghiên Cứu

Trong dự báo chuỗi thời gian nhiều chiều (multivariate time series forecasting), các mô hình dựa trên kiến trúc Transformer truyền thống thường gặp một số hạn chế lớn do cách mã hóa dữ liệu:
1. **Chia nhỏ thời gian thành các token**: Transformer truyền thống coi các giá trị của toàn bộ các biến tại cùng một thời điểm (time step) là một token. Tuy nhiên, các biến này thường đại diện cho các đại lượng vật lý khác nhau (ví dụ: nhiệt độ, độ ẩm, tốc độ gió, nhu cầu thuê xe) nên việc gộp chung chúng vào một token làm loãng thông tin và khiến mô hình khó học được các đặc trưng riêng biệt của từng biến.
2. **Khai thác tương quan chưa hiệu quả**: Cơ chế Self-Attention trong Transformer truyền thống chủ yếu tìm mối quan hệ giữa các bước thời gian (temporal relations) chứ không tập trung vào việc học mối liên hệ qua lại giữa các biến với nhau (cross-variable correlations). Trong khi đó, các biến đổi theo thời gian thường có thể được mô hình hóa khá tốt bằng các lớp tuyến tính đơn giản, còn tương quan giữa các biến mới là thứ phức tạp và quan trọng.

## Ý Tưởng Chính

Bài báo đề xuất một cách tiếp cận đảo ngược cực kỳ đơn giản nhưng hiệu quả gọi là **iTransformer**:
- Thay vì gom các biến tại một thời điểm làm token, mô hình đảo ngược lại: coi toàn bộ chuỗi lịch sử của **một biến số duy nhất** là một token (tức là một thực thể độc lập).
- Nếu dữ liệu có $N$ biến và độ dài lịch sử là $L$, mô hình sẽ làm việc với $N$ token, mỗi token có số chiều ban đầu là $L$. Cách đảo ngược này giúp cấu trúc Self-Attention tập trung hoàn toàn vào việc học mối quan hệ tương quan giữa các biến, còn các thông tin biến đổi theo thời gian sẽ được xử lý riêng cho từng biến bằng mạng Feed-Forward (FFN).

## Mô Hình Đề Xuất

Kiến trúc của iTransformer bao gồm các bước xử lý chính sau:
1. **Mã hóa đặc trưng (Embedding)**: Mỗi chuỗi lịch sử có độ dài $L$ của từng biến được đưa qua một lớp Linear để nhúng (embed) thành một vector có số chiều $D$.
2. **Inverted Self-Attention**: Áp dụng cơ chế Self-Attention trên $N$ token (tương ứng với $N$ biến). Bước này giúp mô hình tính toán trọng số attention giữa các biến, từ đó tìm ra mối liên hệ tương quan giữa các yếu tố (ví dụ: nhiệt độ ảnh hưởng thế nào đến độ ẩm và lượng xe thuê).
3. **Inverted Feed-Forward Network (FFN)**: Sử dụng các lớp MLP/FFN được chia sẻ chung cho tất cả các biến. Mạng này nhận đầu vào là vector đặc trưng của từng biến và học các quy luật biến đổi theo thời gian của biến đó. Việc chia sẻ tham số giúp mô hình hạn chế quá khớp.
4. **Layer Normalization**: Chuẩn hóa được thực hiện dọc theo chiều thời gian của từng biến, giúp giảm thiểu tác động của hiện tượng trôi phân phối (distribution shift) - một vấn đề rất phổ biến trong chuỗi thời gian thực tế.

## Kết Quả Chính

- Đạt hiệu quả vượt trội (State-of-the-Art) trên hầu hết các bộ dữ liệu benchmark lớn về chuỗi thời gian nhiều chiều (Weather, Traffic, Electricity, Exchange,...).
- Khắc phục được điểm yếu của các Transformer truyền thống: hiệu năng của iTransformer tiếp tục cải thiện khi tăng độ dài cửa sổ lịch sử (lookback window), không bị giảm sút do quá khớp hay nhiễu.
- Thể hiện khả năng tổng quát hóa cực kỳ tốt khi huấn luyện trên một số lượng biến nhất định nhưng vẫn có thể suy diễn trực tiếp trên một tập biến khác mà không cần thay đổi cấu trúc.

## Điểm Mạnh

- Khai thác rất tốt và trực quan mối quan hệ tương quan giữa các biến số khác nhau trong hệ thống nhiều chiều.
- Khả năng chống trôi phân phối cực kỳ mạnh mẽ nhờ cơ chế chuẩn hóa theo chiều thời gian của từng biến độc lập.
- Tận dụng tốt nguồn dữ liệu lịch sử dài (lookback window lớn) để nâng cao độ chính xác dự báo.

## Hạn Chế

- Chi phí tính toán của cơ chế Self-Attention tăng theo bình phương số lượng biến ($O(N^2)$). Nếu số lượng biến đầu vào quá lớn (hàng trăm hoặc hàng nghìn biến), mô hình sẽ ngốn rất nhiều bộ nhớ và thời gian chạy.
- Đối với các bộ dữ liệu mà các biến số hoàn toàn độc lập hoặc không có sự tương quan đáng kể, việc áp dụng cơ chế attention giữa các biến có thể không đem lại hiệu quả vượt trội so với các mô hình đơn biến (univariate).

## Khả Năng Áp Dụng Cho Bài Toán Của Nhóm

- Bộ dữ liệu dự báo nhu cầu thuê xe đạp của nhóm là một bài toán chuỗi thời gian nhiều chiều điển hình. Chúng ta có nhiều biến đầu vào có tính chất hoàn toàn khác nhau (thời tiết, nhiệt độ, độ ẩm, tốc độ gió, và các mốc thời gian) cùng tác động lên một biến mục tiêu duy nhất là lượng xe thuê (`cnt`).
- Ý tưởng của iTransformer giúp nhóm nhận thức rõ rằng:
  1. Việc chuẩn hóa dữ liệu theo chiều thời gian cho từng biến là cực kỳ quan trọng để tránh trôi phân phối.
  2. Cần phải chú trọng phân tích mối tương quan giữa các biến thời tiết, thời gian với lượng xe thuê (EDA ma trận tương quan) vì đây là các yếu tố quyết định đến hiệu năng dự báo.
- Dù trong phạm vi đồ án này nhóm ưu tiên triển khai GRU/LSTM để đảm bảo tiến độ và tính khả thi trong lập trình, nhưng lý thuyết từ bài báo iTransformer sẽ được dùng làm cơ sở vững chắc để thiết kế và lập luận về cách chọn biến đầu vào cho mô hình học máy.
