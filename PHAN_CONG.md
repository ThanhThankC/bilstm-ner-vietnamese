# BẢNG PHÂN CÔNG NHIỆM VỤ VÀ TÀI LIỆU ĐẶC TẢ GIAO TIẾP (API CONTRACT)

**Dự án:** Hệ thống Nhận diện Thực thể (NER) sử dụng kiến trúc BiLSTM
**Thời gian dự kiến:** 4 Tuần
**Quy mô nhân sự:** 6 Thành viên

---

## PHẦN 1: PHÂN CÔNG NHIỆM VỤ CHI TIẾT

### 1. Nhóm Dữ liệu (Data Team) - 3 Thành viên: [Ngọc_Bảo], [Quốc_Bảo], [Nhật_Đức]
**Vai trò:** Chịu trách nhiệm cốt lõi trong việc chuẩn bị và đảm bảo chất lượng tập dữ liệu huấn luyện.
* **Nghiên cứu & Chuẩn hóa:** Thống nhất danh sách các nhãn thực thể (PER, LOC, ORG) và áp dụng nghiêm ngặt bộ quy tắc gán nhãn theo định dạng BIO (Begin - Inside - Outside).
* **Thu thập dữ liệu:** Trích xuất khoảng 1000 - 3000 câu văn tiếng Việt từ các nguồn tin cậy như báo chí, Wikipedia.
* **Gán nhãn (Annotation):** Sử dụng các công cụ chuyên dụng như Label Studio hoặc Doccano để gán nhãn dữ liệu đồng nhất. Yêu cầu không thực hiện thao tác này thủ công bằng mã nguồn.
* **Bàn giao:** Xuất dữ liệu dưới định dạng tệp `dataset.json` theo đúng tiêu chuẩn và chuyển giao cho Nhóm Mô hình.

### 2. Nhóm Mô hình và Thuật toán (Model Team) - 1 Thành viên: [Đình_Thanh]
**Vai trò:** Thiết kế kiến trúc thuật toán và phát triển mô hình học máy.
* **Phát triển kiến trúc:** Lập trình lớp `BiLSTM_NER` sử dụng framework PyTorch, lưu độc lập trong tệp `model.py`.
* **Nắm bắt luồng xử lý:** Hiểu rõ cơ chế truyền dữ liệu qua các lớp (Embedding -> BiLSTM -> Linear) nhằm phục vụ cho việc báo cáo trước giảng viên hướng dẫn.
* **Bàn giao:** Chuyển giao lớp `BiLSTM_NER` hoàn thiện để Nhóm Huấn luyện tích hợp.

### 3. Nhóm Huấn luyện và Đánh giá (Training Team) - 1 Thành viên: [Tuấn_Tú]
**Vai trò:** Thực hiện quá trình huấn luyện mô hình, theo dõi hiệu suất và lưu trữ các tham số tối ưu.
* **Tiền xử lý dữ liệu:** Lập trình module đọc tập tin `dataset.json`. Xây dựng bộ từ điển `word_to_ix` (yêu cầu bổ sung token `<UNK>` cho các từ vựng ngoài tập huấn luyện).
* **Huấn luyện mô hình:** Phát triển tập lệnh `train.py`. Thực hiện khởi tạo mô hình, thiết lập vòng lặp huấn luyện (Epochs) và tính toán hàm mất mát (Loss).
* **Đánh giá và lưu trữ:** Trực quan hóa tiến trình huấn luyện qua biểu đồ Loss phục vụ báo cáo. Thực hiện lưu trữ trọng số mô hình dưới định dạng `.pth`.
* **Bàn giao:** Cung cấp bộ 3 tập tin: `model_weights.pth`, `vocab.json`, và `tags.json` cho Nhóm Giao diện.

### 4. Nhóm Giao diện và Tích hợp (UI/Integration Team) - 1 Thành viên: [Đức_Linh]
**Vai trò:** Xây dựng giao diện tương tác người dùng và tích hợp mô hình vào hệ thống phần mềm.
* **Phát triển giao diện:** Xây dựng ứng dụng web tại tệp `app.py` sử dụng thư viện Gradio.
* **Tích hợp mô hình:** Nghiêm cấm đặt mã nguồn huấn luyện tại tệp này. Xây dựng hàm khởi tạo cấu trúc mô hình, sau đó nạp trọng số từ `model_weights.pth` để thực hiện dự đoán (Inference).
* **Xử lý hiển thị:** Tiếp nhận kết quả từ mô hình dự đoán, chuyển đổi mã ID về nhãn thực tế (Ví dụ: B-PER, I-LOC) và làm nổi bật trên giao diện trực quan.

---

## PHẦN 2: TÀI LIỆU ĐẶC TẢ GIAO TIẾP (API CONTRACT)
*Lưu ý: Đây là tài liệu quy định tiêu chuẩn bắt buộc. Các thành viên có trách nhiệm đảm bảo mã nguồn tuân thủ đúng định dạng dưới đây nhằm tránh lỗi hệ thống và xung đột dữ liệu trong quá trình ghép nối.*

### Giao thức 1: Định dạng dữ liệu đầu vào (Từ Nhóm Dữ liệu tới Nhóm Huấn luyện -[Ngọc_Bảo], [Quốc_Bảo], [Nhật_Đức] -> [Tuấn_Tú])
Nhóm Huấn luyện chỉ tiếp nhận dữ liệu định dạng JSON chứa cấu trúc danh sách (List) các đối tượng từ điển (Dictionary) theo đúng quy chuẩn sau:

```json
[
  {
    "tokens": ["ông", "Phạm", "Nhật", "Vượng", "đi", "Hà", "Nội"],
    "labels": ["O", "B-PER", "I-PER", "I-PER", "O", "B-LOC", "I-LOC"]
  },
  {
    "tokens": ["đại", "học", "bách", "khoa"],
    "labels": ["B-ORG", "I-ORG", "I-ORG", "I-ORG"]
  }
]
```
*(Yêu cầu kỹ thuật: Số lượng phần tử trong mảng "tokens" và mảng "labels" bắt buộc phải bằng nhau tuyệt đối).*

### Giao thức 2: Tích hợp mô hình (Từ Nhóm Huấn luyện tới Nhóm Giao diện -[Tuấn_Tú] -> [Đức_Linh])
Để đảm bảo ứng dụng `app.py` có thể vận hành dự đoán độc lập mà không cần thực thi lại mã huấn luyện, Nhóm Huấn luyện có trách nhiệm cung cấp 3 tập tin sau vào thư mục `models/`:
* `bilstm_weights.pth`: Tập tin chứa trọng số mạng nơ-ron đã được huấn luyện.
* `word_vocab.json`: Từ điển ánh xạ từ vựng sang số nguyên định danh (Bắt buộc phải bao gồm key `<UNK>`).
* `tag_vocab.json`: Từ điển ánh xạ nhãn dự đoán sang số nguyên (Ví dụ: `{"O": 0, "B-PER": 1, ...}`) phục vụ quá trình dịch ngược định dạng.

Hàm xử lý dự đoán tại Nhóm Giao diện cần tuân thủ cấu trúc tham số và giá trị trả về như sau:
`def predict(text_input: str) -> list of tuples:`
*(Ví dụ định dạng trả về hợp lệ: `[("ông ", None), ("Phạm ", "PER")]`)*