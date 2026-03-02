# 🏷️ Hệ thống Nhận diện Thực thể (NER) Tiếng Việt với BiLSTM

Chào mừng đến với dự án Hệ thống Nhận diện Thực thể (Named Entity Recognition - NER) dành cho tiếng Việt. Dự án này được xây dựng từ đầu (from scratch) sử dụng kiến trúc mạng nơ-ron BiLSTM kết hợp với PyTorch và giao diện Web trực quan bằng Gradio.

## 🌟 Giới thiệu tổng quan
Hệ thống có khả năng phân tích một câu văn tiếng Việt và tự động trích xuất các thực thể quan trọng bao gồm:
* **PER (Person):** Tên người (Ví dụ: Phạm Nhật Vượng)
* **LOC (Location):** Địa điểm, vị trí (Ví dụ: Hà Nội, đại cồ việt)
* **ORG (Organization):** Tên tổ chức, cơ quan (Ví dụ: đại học bách khoa)

Mô hình học máy cốt lõi được xây dựng hoàn toàn độc lập, cho phép nhóm nắm vững luồng đi của tensor qua các lớp `Embedding`, `BiLSTM` và `Linear`, thay vì phụ thuộc vào các thư viện đóng gói sẵn (black-box).

---

## 💻 Yêu cầu Hệ thống & Cài đặt

Dự án được phân chia cho 4 nhóm nhỏ với yêu cầu cấu hình phần cứng và phần mềm khác nhau:

| Tên Team          | Số người | Yêu cầu máy tính (Hardware) | Cài đặt cần thiết (Software)        |
| :---              | :---     | :---                        | :---                                |
| **Team Data**     | 3 người  | Rất nhẹ (Máy tính văn phòng bình thường) | Không cần code. Chỉ cần trình duyệt Web vào Label Studio/Doccano. |
| **Team Model**    | 1 người  | Trung bình (RAM 8GB trở lên)| VS Code, Python, thư viện `torch`. Không cần Gradio. |
| **Team Training** | 1 người  | Mạnh nhất (Nên có Card rời GPU hoặc dùng Google Colab). Máy yếu chạy sẽ rất lâu và nóng. | VS Code, Python, `torch`. |
| **Team UI**       | 1 người  | Trung bình                  | VS Code, Python, `torch`, `gradio`. |

---

## 🚀 Hướng dẫn chạy dự án trên máy tính

### Bước 1: Cài đặt thư viện
Đảm bảo bạn đã kích hoạt môi trường ảo (`venv`). Sau đó mở Terminal và chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install torch gradio