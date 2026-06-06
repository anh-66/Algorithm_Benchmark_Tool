# CÔNG CỤ SO SÁNH HIỆU NĂNG CÁC GIẢI THUẬT SẮP XẾP (ALGORITHM BENCHMARK TOOL)

Môn học: Phân tích thiết kế giải thuật
Đồ án cuối kỳ - Chủ đề 12

## Giới thiệu dự án
Ứng dụng cho phép trực quan hóa và so sánh đồng thời 4 giải thuật sắp xếp dựa trên các bộ dữ liệu đầu vào khác nhau (Ngẫu nhiên, Đã sắp xếp một phần, Sắp xếp ngược). Hệ thống tự động phân tích và đưa ra báo cáo thuật toán tối ưu nhất sau khi chạy xong.

## Thành viên thực hiện


## Các giải thuật cài đặt cốt lõi (Tự viết tay 100%)
1. **Bubble Sort** (Sắp xếp nổi bọt)
2. **Insertion Sort** (Sắp xếp chèn)
3. **Merge Sort** (Sắp xếp trộn)
4. **Quick Sort** (Sắp xếp nhanh - sử dụng kỹ thuật chọn pivot ngẫu nhiên)

## Cấu trúc thư mục dự án
```text
algorithm_benchmark_tool/
├── core/               # Chứa logic cốt lõi tự cài đặt của các giải thuật
├── ui/                 # Giao diện chính và các panel hiển thị biểu đồ
├── workers/            # Quản lý đa luồng (QThread) xử lý chạy song song
├── utils/              # Bộ tạo dữ liệu thử nghiệm (Random, Nearly Sorted, Reversed)
├── main.py             # Điểm chạy chính của ứng dụng
└── requirements.txt    # Các thư viện phụ thuộc