import torch
import torch.nn as nn
import torch.optim as optim
import json
from model import BiLSTM_NER # Gọi bộ não từ file model.py sang

print("1. Đang đọc dữ liệu từ dataset.json...")
with open("data\dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

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

print("2. Đang khởi tạo mô hình...")
EMBEDDING_DIM = 6
HIDDEN_DIM = 6
model = BiLSTM_NER(len(word_to_ix), len(tag_to_ix), EMBEDDING_DIM, HIDDEN_DIM)
loss_function = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

print("3. Bắt đầu huấn luyện...")
for epoch in range(300):
    for item in data:
        model.zero_grad()
        sentence_in = prepare_sequence(item["tokens"], word_to_ix)
        targets = prepare_sequence(item["labels"], tag_to_ix)
        tag_scores = model(sentence_in)
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()

print("4. Huấn luyện xong! Đang lưu lại sự thông minh của AI...")

# Lưu trọng số mô hình vào thư mục src
torch.save(model.state_dict(), "models/bilstm_weights.pth")

# Lưu từ điển vào thư mục src
with open("models/word_vocab.json", "w", encoding="utf-8") as f:
    json.dump(word_to_ix, f, ensure_ascii=False, indent=4)
with open("models/tag_vocab.json", "w", encoding="utf-8") as f:
    json.dump(tag_to_ix, f, ensure_ascii=False, indent=4)
    
print("XONG! Đã sinh ra 3 file: bilstm_weights.pth, word_vocab.json, tag_vocab.json.")