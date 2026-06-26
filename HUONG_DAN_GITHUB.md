# Hướng Dẫn Clone Repo, Làm Việc Và Push Lên GitHub

Tài liệu này hướng dẫn các thành viên nhóm 06 cách clone repository về máy, làm việc trên branch riêng, commit, push và tạo Pull Request.

## 1. Link Repository

Repository của nhóm:

```text
https://github.com/npthieu-2502/time-series-group-06
```

Link clone:

```text
https://github.com/npthieu-2502/time-series-group-06.git
```

## 2. Clone Repository Về Máy

Mỗi thành viên mở Terminal, Git Bash hoặc PowerShell tại thư mục muốn lưu project, sau đó chạy:

```bash
git clone https://github.com/npthieu-2502/time-series-group-06.git
```

Sau khi clone xong, di chuyển vào thư mục project:

```bash
cd time-series-group-06
```

Kiểm tra trạng thái Git:

```bash
git status
```

Nếu thấy đang ở branch `main` và working tree clean là đúng.

## 3. Quy Tắc Làm Việc

Các thành viên cần tuân thủ:

```text
1. Không sửa trực tiếp trên branch main.
2. Mỗi người tạo branch riêng cho phần việc của mình.
3. Trước khi tạo branch mới, luôn cập nhật main mới nhất.
4. Chỉ sửa đúng file thuộc phần việc của mình.
5. Sau khi làm xong, push branch lên GitHub.
6. Tạo Pull Request để trưởng nhóm kiểm tra và merge vào main.
```

## 4. Cập Nhật Code Mới Nhất Từ Main

Trước khi bắt đầu làm, chạy:

```bash
git checkout main
git pull origin main
```

Lệnh này giúp máy của bạn có phiên bản mới nhất từ GitHub.

## 5. Tạo Branch Riêng

Mỗi thành viên tạo branch riêng theo phần việc.

### Thành viên 1: Paper iTransformer Và EDA

```bash
git checkout -b feature/data-exploration
```

Các file cần làm:

```text
papers/paper_01_itransformer.md
notebooks/01_data_exploration.ipynb
figures/eda_*.png
```

### Thành viên 2: Paper TimeMixer Và Feature Engineering

```bash
git checkout -b feature/feature-engineering
```

Các file cần làm:

```text
papers/paper_02_timemixer.md
notebooks/02_feature_engineering.ipynb
src/features.py
data/processed/bike_sharing_processed.csv
```

### Thành viên 3: Paper xLSTM-Mixer, Mô Hình Và Đánh Giá

```bash
git checkout -b feature/models-evaluation
```

Các file cần làm:

```text
papers/paper_03_xlstm_mixer.md
notebooks/03_models.ipynb
notebooks/04_evaluation.ipynb
src/models.py
src/evaluation.py
results/metrics.csv
figures/y_true_vs_y_pred.png
```

## 6. Kiểm Tra File Đã Sửa

Sau khi làm xong một phần, kiểm tra các file đã thay đổi:

```bash
git status
```

Xem chi tiết thay đổi:

```bash
git diff
```

Với notebook `.ipynb`, `git diff` có thể khó đọc. Chỉ cần đảm bảo notebook đã được lưu trước khi commit.

## 7. Add Và Commit

Add toàn bộ thay đổi:

```bash
git add .
```

Commit với nội dung rõ ràng:

```bash
git commit -m "Add data exploration notebook"
```

Ví dụ commit message tốt:

```text
Add iTransformer paper summary
Add data exploration notebook
Add feature engineering pipeline
Add baseline forecasting models
Add model evaluation metrics
Update final report
```

Không nên commit message quá chung chung như:

```text
update
fix
done
abc
```

## 8. Push Branch Lên GitHub

Sau khi commit, push branch của mình lên GitHub.

Ví dụ với branch `feature/data-exploration`:

```bash
git push origin feature/data-exploration
```

Ví dụ với branch `feature/feature-engineering`:

```bash
git push origin feature/feature-engineering
```

Ví dụ với branch `feature/models-evaluation`:

```bash
git push origin feature/models-evaluation
```

## 9. Tạo Pull Request

Sau khi push, mở repository trên GitHub:

```text
https://github.com/npthieu-2502/time-series-group-06
```

GitHub thường sẽ hiện nút:

```text
Compare & pull request
```

Bấm vào nút đó.

Nếu không thấy nút, làm thủ công:

```text
Pull requests -> New pull request
```

Chọn:

```text
base: main
compare: branch của bạn
```

Ví dụ:

```text
base: main
compare: feature/data-exploration
```

Sau đó nhập tiêu đề Pull Request, ví dụ:

```text
Add data exploration and iTransformer summary
```

Rồi bấm:

```text
Create pull request
```

## 10. Trưởng Nhóm Review Và Merge

Trưởng nhóm kiểm tra Pull Request:

- File có đúng phần việc không.
- Notebook có chạy được không.
- Có sửa nhầm file của người khác không.
- Nội dung có đúng yêu cầu bài tập không.

Nếu ổn, trưởng nhóm bấm:

```text
Merge pull request
```

Sau đó bấm:

```text
Confirm merge
```

## 11. Sau Khi Pull Request Được Merge

Sau khi branch của bạn đã được merge vào `main`, cập nhật lại code trên máy:

```bash
git checkout main
git pull origin main
```

Nếu cần làm phần mới, tạo branch mới từ `main`:

```bash
git checkout -b feature/report
```

## 12. Cách Xử Lý Khi Bị Lỗi Remote Hoặc Push

Kiểm tra remote hiện tại:

```bash
git remote -v
```

Remote đúng phải là:

```text
https://github.com/npthieu-2502/time-series-group-06.git
```

Nếu sai, sửa lại:

```bash
git remote set-url origin https://github.com/npthieu-2502/time-series-group-06.git
```

Sau đó push lại:

```bash
git push origin ten-branch-cua-ban
```

## 13. Quy Trình Tóm Tắt

Mỗi lần làm việc, các thành viên làm theo quy trình:

```text
git checkout main
git pull origin main
git checkout -b feature/ten-phan-viec

Làm và lưu file

git status
git add .
git commit -m "Mô tả thay đổi"
git push origin feature/ten-phan-viec

Lên GitHub tạo Pull Request vào main
```

## 14. Lưu Ý Khi Làm Notebook

Trước khi commit notebook:

- Chạy lại các cell quan trọng.
- Lưu notebook.
- Xóa output quá dài nếu có.
- Không lưu file tạm không cần thiết.

Các notebook chính:

```text
notebooks/01_data_exploration.ipynb
notebooks/02_feature_engineering.ipynb
notebooks/03_models.ipynb
notebooks/04_evaluation.ipynb
```

## 15. Lưu Ý Về Dataset

File dữ liệu gốc đặt tại:

```text
data/raw/hour.csv
```

Nếu Git không push file CSV do `.gitignore`, nhóm có thể:

1. Ghi rõ link tải dataset trong README.
2. Không push dataset gốc lên GitHub.
3. Hoặc sửa `.gitignore` nếu giảng viên yêu cầu nộp cả file dữ liệu.

Dataset sử dụng:

```text
UCI Bike Sharing Dataset
https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
```
