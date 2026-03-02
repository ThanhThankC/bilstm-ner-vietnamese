import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(1) # Cố định seed để kết quả ổn định

# =====================================================================
# 1. PHẦN CỦA TEAM DATA: Chuẩn bị dữ liệu huấn luyện
# Nhiệm vụ thực tế: Team Data phải làm ra khoảng 1000 - 5000 câu như thế này.
# =====================================================================
training_data = [
    ("hôm nay ông vượng đi hà nội".split(), ["O", "O", "O", "PER", "O", "LOC", "LOC"]),
    ("trường bách khoa nằm ở đường đại cồ việt".split(), ["ORG", "ORG", "ORG", "O", "O", "LOC", "LOC", "LOC", "LOC"])
]

# Tạo bộ từ điển (Vocab) cho Từ và Nhãn
word_to_ix = {} # Từ điển chuyển Chữ -> Số ID
for sentence, tags in training_data:
    for word in sentence:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)

tag_to_ix = {"O": 0, "PER": 1, "LOC": 2, "ORG": 3} # 4 Nhãn cơ bản

# Hàm phụ trợ: Chuyển câu văn thành tensor số (Team Tiền xử lý lo phần này)
def prepare_sequence(seq, to_ix):
    idxs = [to_ix.get(w, 0) for w in seq] # Nếu từ lạ không có trong vocab thì mặc định gán 0
    return torch.tensor(idxs, dtype=torch.long)

# =====================================================================
# 2. PHẦN CỦA TEAM MODEL: Xây dựng kiến trúc BiLSTM 
# Nhiệm vụ thực tế: Hiểu rõ từng lớp tính toán cái gì để lên chém gió với cô.
# =====================================================================
class BiLSTM_NER(nn.Module):
    def __init__(self, vocab_size, tagset_size, embedding_dim, hidden_dim):
        super(BiLSTM_NER, self).__init__()
        self.hidden_dim = hidden_dim

        # Lớp 1: Embedding - Biến mỗi ID từ vựng thành 1 vector đặc trưng
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # Lớp 2: BiLSTM - Đọc câu từ Trái sang Phải và Phải sang Trái
        # Đây chính là "sự thông minh" giúp AI hiểu ngữ cảnh xung quanh một từ
        self.lstm = nn.LSTM(embedding_dim, hidden_dim // 2, num_layers=1, bidirectional=True)

        # Lớp 3: Linear - Nhận kết quả từ BiLSTM và chấm điểm cho 4 loại Nhãn
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, _ = self.lstm(embeds.view(len(sentence), 1, -1))
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        # Trả về ma trận điểm số của từng từ đối với từng nhãn
        return tag_space

# Khởi tạo mô hình
EMBEDDING_DIM = 6
HIDDEN_DIM = 6
model = BiLSTM_NER(len(word_to_ix), len(tag_to_ix), EMBEDDING_DIM, HIDDEN_DIM)

# =====================================================================
# 3. PHẦN CỦA TEAM TRAINING: Dạy cho AI học
# Nhiệm vụ thực tế: Canh chừng quá trình học, vẽ biểu đồ Loss, tối ưu tham số (lr).
# =====================================================================
loss_function = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

print("--- ĐANG HUẤN LUYỆN (TRAINING) ---")
for epoch in range(300): # Cho máy học 300 vòng
    total_loss = 0
    for sentence, tags in training_data:
        model.zero_grad() # Xóa rác của vòng lặp trước
        
        # Tiền xử lý đầu vào và đáp án
        sentence_in = prepare_sequence(sentence, word_to_ix)
        targets = prepare_sequence(tags, tag_to_ix)
        
        # Đưa câu vào model để dự đoán (Forward)
        tag_scores = model(sentence_in)
        
        # Tính sai số (Loss) và tự cập nhật file trọng số (Backward)
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        
    if epoch % 50 == 0:
        print(f"Vòng {epoch} | Sai số (Loss): {total_loss:.4f}")

print("\n--- HOÀN THÀNH HUẤN LUYỆN ---")

# =====================================================================
# 4. PHẦN CỦA TEAM UI: Kiểm tra và Ghép vào Giao diện Web
# Nhiệm vụ thực tế: Tích hợp đoạn test này vào hàm nhan_dien_thuc_the trong file app.py
# =====================================================================
print("\n--- KIỂM TRA THỰC TẾ (INFERENCE) ---")
test_sentence = "ông vượng ở đại cồ việt".split() # Câu này AI chưa từng học y hệt
print(f"Câu đầu vào: {test_sentence}")

with torch.no_grad(): # Tắt tính đạo hàm đi cho nhẹ máy khi test
    inputs = prepare_sequence(test_sentence, word_to_ix)
    tag_scores = model(inputs)
    
    # Tìm nhãn có điểm số cao nhất (argmax)
    predicted_tags_idx = torch.argmax(tag_scores, dim=1).tolist()

# Dịch ngược ID số thành Tên Nhãn
ix_to_tag = {v: k for k, v in tag_to_ix.items()}
for word, tag_id in zip(test_sentence, predicted_tags_idx):
    print(f"Từ: [{word}] --> Nhãn: {ix_to_tag[tag_id]}")