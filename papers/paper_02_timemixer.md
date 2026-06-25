# Paper 02: TimeMixer

## Tên Bài Báo

TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting

## Vấn Đề Nghiên Cứu

Trong dự báo chuỗi thời gian, dữ liệu thực tế thường chứa đan xen nhiều thành phần có bản chất hoàn toàn khác nhau: xu hướng dài hạn (trend) biến đổi chậm theo nhiều tuần hoặc nhiều tháng, tính mùa vụ (seasonality) lặp đi lặp lại theo giờ, ngày hoặc tuần, và các biến động ngẫu nhiên (fluctuation) ngắn hạn khó đoán. Điểm mấu chốt của vấn đề là mỗi thành phần này lại nổi bật ở một thang đo thời gian (scale) khác nhau.

Các mô hình hiện có như Transformer, LSTM hay TCN thường xử lý chuỗi thời gian ở **một thang đo duy nhất**. Hệ quả là nếu mô hình nhìn vào độ phân giải cao (fine scale), nó dễ bị nhiễu bởi các biến động ngắn hạn và khó nhận ra xu hướng vĩ mô; ngược lại, nếu chỉ nhìn ở độ phân giải thấp (coarse scale), nó sẽ bỏ mất các chi tiết chu kỳ nhỏ quan trọng. Không có thang đo nào đơn lẻ nào đủ để nắm bắt toàn bộ cấu trúc phức tạp của chuỗi thời gian thực tế.

## Ý Tưởng Chính

TimeMixer xuất phát từ một quan sát đơn giản nhưng sâu sắc: **thông tin vi mô** (biến động và mùa vụ ngắn hạn) thể hiện rõ ràng ở thang đo nhỏ (fine scale), trong khi **thông tin vĩ mô** (xu hướng dài hạn) nổi bật ở thang đo lớn (coarse scale). Thay vì phải chọn một trong hai, TimeMixer khai thác cả hai cùng lúc bằng cách xây dựng một biểu diễn đa thang đo (multiscale representation) và thiết kế hai cơ chế trộn thông tin (mixing) chuyên biệt để giao tiếp qua lại giữa các thang đo này.

Điểm đặc biệt là toàn bộ kiến trúc chỉ dùng **MLP (Multi-Layer Perceptron)** đơn giản — không có cơ chế Self-Attention tốn kém, không có Convolution phức tạp — nhưng vẫn đạt hiệu năng vượt trội. Điều này chứng minh rằng việc thiết kế đúng *cấu trúc phân tích dữ liệu* quan trọng hơn việc dùng kiến trúc phức tạp.

## Mô Hình Đề Xuất

Kiến trúc của TimeMixer bao gồm hai khối xử lý chính:

1. **Phân rã và trộn thông tin quá khứ (Past-Decomposable-Mixing — PDM)**: Chuỗi lịch sử đầu vào được biến đổi thành $M$ phiên bản có độ phân giải giảm dần thông qua average pooling. Tại mỗi thang đo, chuỗi được phân rã thành thành phần xu hướng (dùng làm mượt) và thành phần mùa vụ (phần còn lại). Sau đó, PDM thực hiện hai chiều trộn thông tin: **Fine-to-Coarse** gộp chi tiết mùa vụ ngắn hạn từ thang mịn bổ sung lên thang thô, và **Coarse-to-Fine** đưa thông tin xu hướng dài hạn từ thang thô xuống điều chỉnh lại thang mịn. Nhờ vậy, mỗi thang đo không còn "nhìn riêng lẻ" mà được làm giàu bởi thông tin từ các thang đo khác.

2. **Tổng hợp nhiều bộ dự báo trong tương lai (Future-Multipredictor-Mixing — FMM)**: Thay vì dùng một bộ dự báo duy nhất, mỗi thang đo có một bộ MLP riêng tạo ra một dự báo độc lập. Các dự báo này sau đó được kết hợp theo kiểu ensemble, tận dụng thế mạnh của từng thang đo: bộ dự báo ở thang mịn nắm bắt tốt các chu kỳ ngắn hạn, bộ dự báo ở thang thô nắm bắt tốt xu hướng dài hạn. Kết quả cuối cùng là sự tổng hợp cân bằng của tất cả các góc nhìn.

## Kết Quả Chính

- Đạt hiệu quả vượt trội (State-of-the-Art) trên nhiều bộ dữ liệu benchmark lớn về cả dự báo dài hạn lẫn ngắn hạn (ETTh1, ETTh2, ETTm1, ETTm2, Weather, Traffic, Exchange Rate).
- Cải thiện đáng kể cả MSE lẫn MAE so với các mô hình cùng thời như PatchTST, DLinear, TimesNet và iTransformer.
- Tốc độ huấn luyện nhanh và chi phí bộ nhớ thấp hơn hẳn so với các mô hình dùng Self-Attention, nhờ kiến trúc MLP thuần túy tránh được độ phức tạp $O(T^2)$.
- Hoạt động hiệu quả trên cả bài toán dự báo đơn biến lẫn đa biến mà không cần thay đổi kiến trúc.

## Điểm Mạnh

- Khai thác đồng thời thông tin ở nhiều thang đo thời gian, giúp mô hình nắm bắt cả mùa vụ ngắn hạn lẫn xu hướng dài hạn một cách tự nhiên mà không cần can thiệp thủ công.
- Kiến trúc đơn giản, chỉ dùng MLP, dễ huấn luyện và tiết kiệm tài nguyên hơn nhiều so với các mô hình dựa trên Transformer.
- Cơ chế FMM ensemble nhiều bộ dự báo giúp tăng độ chính xác và tính ổn định của kết quả cuối cùng.
- Không phụ thuộc vào positional encoding nên không bị giới hạn bởi độ dài chuỗi như các kiến trúc Transformer.

## Hạn Chế

- Hiệu năng phụ thuộc vào việc chọn số thang đo $M$ và tỉ lệ downsampling phù hợp — đây là các siêu tham số cần tinh chỉnh cẩn thận cho từng bộ dữ liệu.
- Giả định ngầm rằng chuỗi thời gian đầu vào có tính chu kỳ hoặc xu hướng rõ ràng. Nếu dữ liệu hoàn toàn là nhiễu ngẫu nhiên, lợi thế của phân rã đa thang đo sẽ giảm đi đáng kể.
- Không có cơ chế học tương quan giữa các biến một cách tường minh như iTransformer. Mô hình phụ thuộc vào MLP để học ngầm các mối quan hệ này, vốn kém minh bạch và có thể kém hiệu quả khi tương quan giữa các biến là phức tạp.

## Khả Năng Áp Dụng Cho Bài Toán Của Nhóm

- Bộ dữ liệu nhu cầu thuê xe đạp của nhóm có cấu trúc đa chu kỳ rất rõ ràng, hoàn toàn phù hợp với triết lý thiết kế của TimeMixer: chu kỳ giờ cao điểm sáng-chiều tương ứng với thang mịn (fine scale) mà PDM khai thác mùa vụ ngắn hạn; chu kỳ ngày trong tuần (thứ 2–6 khác hẳn cuối tuần) là thang trung gian; và xu hướng theo mùa trong năm (mùa xuân-hè nhiều xe hơn thu-đông) chính là thang thô (coarse scale) mà PDM tổng hợp xu hướng dài hạn.
- Ý tưởng của TimeMixer giúp nhóm nhận thức rõ rằng:
  1. Các đặc trưng Fourier (`hour_sin`, `hour_cos`, `month_sin`, `month_cos`, `weekday_sin`, `weekday_cos`) mà nhóm xây dựng chính là cách mã hóa thủ công hành vi đa chu kỳ — tương đương với việc TimeMixer phân tích mùa vụ ở nhiều thang đo khác nhau.
  2. Các lag features (`lag_1`, `lag_24`, `lag_168`) phản ánh trực tiếp cấu trúc đa thang đo: `lag_1` là fine scale (1 giờ), `lag_24` là mid scale (1 ngày), `lag_168` là coarse scale (1 tuần).
  3. Các rolling features (`rolling_mean_24`, `rolling_std_24`) tương đương với thao tác làm mượt dùng trong PDM để trích xuất thành phần xu hướng từ chuỗi gốc.
- Dù trong phạm vi đồ án này nhóm ưu tiên triển khai GRU/LSTM để đảm bảo tiến độ và tính khả thi trong lập trình, nhưng lý thuyết từ bài báo TimeMixer cung cấp cơ sở vững chắc để lý giải tại sao nhóm lựa chọn tập hợp đặc trưng đầu vào như vậy: mỗi nhóm đặc trưng tương ứng với một thang đo thời gian cụ thể mà mô hình cần nắm bắt.
