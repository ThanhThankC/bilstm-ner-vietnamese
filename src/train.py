import torch
import torch.nn as nn
import torch.optim as optim
import json
import os
import glob
from model import BiLSTM_NER # Gọi bộ não từ file model.py sang

print("1. Đang quét và đọc tất cả dữ liệu từ thư mục data/...")
data = []

# Quét tìm tất cả các file có đuôi .json nằm trong thư mục data
danh_sach_file = glob.glob("data/*.json")

if not danh_sach_file:
    print("⚠️ LỖI: Không tìm thấy file .json nào trong thư mục data/!")
    exit()

for file_path in danh_sach_file:
    print(f" -> Đang nạp dữ liệu từ: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        file_data = json.load(f)
        data.extend(file_data) # Gộp dữ liệu của file này vào mảng data tổng

print(f"=> Tổng cộng đã gom được {len(data)} câu để huấn luyện.")

# Tạo từ điển (Thêm <UNK> để xử lý từ lạ)
word_to_ix = {"<UNK>": 0} 
tag_to_ix = {}

for item in data:
    for word in item["tokens"]:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
    for tag in item["labels"]:
        if tag not in tag_to_ix:
            tag_to_ix[tag] = len(tag_to_ix)

def prepare_sequence(seq, to_ix):
    # Dùng if-else list comprehension để tránh lỗi evaluate mặc định của hàm .get()
    idxs = [to_ix[w] if w in to_ix else to_ix["<UNK>"] for w in seq]
    return torch.tensor(idxs, dtype=torch.long)

print("\n2. Đang khởi tạo mô hình...")
EMBEDDING_DIM = 64
HIDDEN_DIM = 128
model = BiLSTM_NER(len(word_to_ix), len(tag_to_ix), EMBEDDING_DIM, HIDDEN_DIM)
loss_function = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

print("3. Bắt đầu huấn luyện...")
for epoch in range(500):
    for item in data:
        model.zero_grad()
        sentence_in = prepare_sequence(item["tokens"], word_to_ix)
        targets = prepare_sequence(item["labels"], tag_to_ix)
        tag_scores = model(sentence_in)
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()

print("4. Huấn luyện xong! Đang lưu lại sự thông minh của AI...")

# Đảm bảo thư mục models/ đã tồn tại trước khi lưu, nếu chưa có thì tự tạo
os.makedirs("models", exist_ok=True)

# Lưu trọng số mô hình vào thư mục models/
torch.save(model.state_dict(), "models/bilstm_weights.pth")

# Lưu từ điển vào thư mục models/
with open("models/word_vocab.json", "w", encoding="utf-8") as f:
    json.dump(word_to_ix, f, ensure_ascii=False, indent=4)
with open("models/tag_vocab.json", "w", encoding="utf-8") as f:
    json.dump(tag_to_ix, f, ensure_ascii=False, indent=4)
    
print("🎉 XONG! Đã sinh ra 3 file: bilstm_weights.pth, word_vocab.json, tag_vocab.json trong thư mục models/.")