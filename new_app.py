import gradio as gr
import torch
import torch.nn as nn
import torch.optim as optim

# =====================================================================
# 1. PHẦN CHUẨN BỊ MÔ HÌNH VÀ DỮ LIỆU (TỪ TEST.PY)
# =====================================================================
print("Đang khởi tạo và huấn luyện mô hình BiLSTM của team...")

torch.manual_seed(1)

training_data = [
    ("hôm nay ông vượng đi hà nội".split(), ["O", "O", "O", "PER", "O", "LOC", "LOC"]),
    ("trường bách khoa nằm ở đường đại cồ việt".split(), ["ORG", "ORG", "ORG", "O", "O", "LOC", "LOC", "LOC", "LOC"])
]

word_to_ix = {} 
for sentence, tags in training_data:
    for word in sentence:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)

tag_to_ix = {"O": 0, "PER": 1, "LOC": 2, "ORG": 3} 
ix_to_tag = {v: k for k, v in tag_to_ix.items()} # Cần cái này để dịch ngược ID ra chữ

def prepare_sequence(seq, to_ix):
    idxs = [to_ix.get(w, 0) for w in seq] 
    return torch.tensor(idxs, dtype=torch.long)

class BiLSTM_NER(nn.Module):
    def __init__(self, vocab_size, tagset_size, embedding_dim, hidden_dim):
        super(BiLSTM_NER, self).__init__()
        self.hidden_dim = hidden_dim
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim // 2, num_layers=1, bidirectional=True)
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, _ = self.lstm(embeds.view(len(sentence), 1, -1))
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        return tag_space

# Khởi tạo và Huấn luyện (Chạy 1 lần khi bật web)
EMBEDDING_DIM = 6
HIDDEN_DIM = 6
model = BiLSTM_NER(len(word_to_ix), len(tag_to_ix), EMBEDDING_DIM, HIDDEN_DIM)

loss_function = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

for epoch in range(300): 
    for sentence, tags in training_data:
        model.zero_grad()
        sentence_in = prepare_sequence(sentence, word_to_ix)
        targets = prepare_sequence(tags, tag_to_ix)
        tag_scores = model(sentence_in)
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()

print("Huấn luyện xong! Đang khởi động giao diện Web...")

# =====================================================================
# 2. PHẦN KẾT NỐI VỚI GIAO DIỆN WEB (CỦA TEAM UI)
# =====================================================================
def nhan_dien_thuc_the(van_ban):
    # Nếu người dùng không nhập gì
    if not van_ban.strip():
        return []
        
    # Tách câu thành các từ (dựa vào khoảng trắng)
    tu_vung = van_ban.split()
    
    with torch.no_grad():
        inputs = prepare_sequence(tu_vung, word_to_ix)
        tag_scores = model(inputs)
        predicted_tags_idx = torch.argmax(tag_scores, dim=1).tolist()
    
    # Định dạng lại kết quả để hiển thị trên Gradio
    hien_thi = []
    
    for i, (tu, tag_id) in enumerate(zip(tu_vung, predicted_tags_idx)):
        nhan = ix_to_tag[tag_id]
        
        # Gradio HighlightedText yêu cầu: nếu không phải thực thể thì nhãn là None
        if nhan == "O":
            nhan_hien_thi = None
        else:
            nhan_hien_thi = nhan
            
        # Thêm khoảng trắng vào sau từ để khi lên web các từ không bị dính liền vào nhau
        tu_kem_khoang_trang = tu + " " if i < len(tu_vung) - 1 else tu
        
        hien_thi.append((tu_kem_khoang_trang, nhan_hien_thi))
        
    return hien_thi

# Xây dựng giao diện Web UI với Gradio
giao_dien = gr.Interface(
    fn=nhan_dien_thuc_the, 
    inputs=gr.Textbox(lines=4, placeholder="Nhập câu tiếng Việt vào đây...", label="Văn bản đầu vào (Input)"),
    outputs=gr.HighlightedText(label="Kết quả nhận diện (Output)"),
    title="Hệ thống Nhận diện Thực thể (NER) - Custom BiLSTM",
    description="Hệ thống tự động nhận diện Tên người (PER), Địa điểm (LOC) và Tổ chức (ORG) chạy bằng mô hình BiLSTM do nhóm tự build.",
    examples=[
        ["hôm nay ông vượng đi hà nội"],
        ["trường bách khoa nằm ở đường đại cồ việt"]
    ] 
)

if __name__ == "__main__":
    giao_dien.launch()