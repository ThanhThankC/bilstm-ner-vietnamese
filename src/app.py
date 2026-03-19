import gradio as gr
import torch
import json
from model import BiLSTM_NER

print("Đang khởi động Web và nạp mô hình đã được huấn luyện...")

# 1. Tải lại Từ điển
with open("models/word_vocab.json", "r", encoding="utf-8") as f:
    word_to_ix = json.load(f)
with open("models/tag_vocab.json", "r", encoding="utf-8") as f:
    tag_to_ix = json.load(f)
ix_to_tag = {v: k for k, v in tag_to_ix.items()}

# 2. Khởi tạo mô hình trống và nhồi trọng số (sự thông minh) vào
EMBEDDING_DIM = 64
HIDDEN_DIM = 128
model = BiLSTM_NER(len(word_to_ix), len(tag_to_ix), EMBEDDING_DIM, HIDDEN_DIM)
model.load_state_dict(torch.load("models/bilstm_weights.pth"))
model.eval() # Bật chế độ làm bài kiểm tra (không học nữa)

# Hàm chuẩn bị đầu vào có xử lý từ lạ (<UNK>)
def prepare_sequence(seq, to_ix):
    idxs = [to_ix.get(w, to_ix["<UNK>"]) for w in seq]
    return torch.tensor(idxs, dtype=torch.long)

# 3. Hàm xử lý logic nhận diện
def nhan_dien_thuc_the(van_ban):
    if not van_ban.strip():
        return []
        
    tu_vung = van_ban.split()
    
    with torch.no_grad():
        inputs = prepare_sequence(tu_vung, word_to_ix)
        tag_scores = model(inputs)
        predicted_tags_idx = torch.argmax(tag_scores, dim=1).tolist()
    
    hien_thi = []
    for i, (tu, tag_id) in enumerate(zip(tu_vung, predicted_tags_idx)):
        nhan = ix_to_tag[tag_id]
        nhan_hien_thi = None if nhan == "O" else nhan
        tu_kem_khoang_trang = tu + " " if i < len(tu_vung) - 1 else tu
        hien_thi.append((tu_kem_khoang_trang, nhan_hien_thi))
        
    return hien_thi

# 4. Giao diện UI
giao_dien = gr.Interface(
    fn=nhan_dien_thuc_the, 
    inputs=gr.Textbox(lines=4, placeholder="Nhập câu vào đây..."),
    outputs=gr.HighlightedText(label="Kết quả nhận diện"),
    title="Hệ thống Nhận diện Thực thể - Nhóm 5 - 69IT5",
    examples=[
        # PER đơn giản
        ["thủ tướng phạm minh chính thăm nhật bản"],
        ["ca sĩ mỹ tâm tổ chức liveshow tại tp hồ chí minh"],
        ["giáo sư nguyễn văn an giảng dạy tại đại học bách khoa hà nội"],
        ["ông trần văn bình được bổ nhiệm làm giám đốc fpt"],
        # LOC
        ["hội nghị thượng đỉnh diễn ra tại singapore"],
        ["tỉnh nghệ an đẩy mạnh phát triển kinh tế"],
        ["đà nẵng và hội an thu hút nhiều khách du lịch"],
        # ORG
        ["samsung khai trương nhà máy mới tại bắc ninh"],
        ["bệnh viện bạch mai tiếp nhận bệnh nhân từ hà nội"],
        ["ubnd tỉnh bình dương họp khẩn về quy hoạch"],
        ["đại học quốc gia hà nội tổ chức lễ tốt nghiệp"],
        # Nhiều entity
        ["elon musk gặp chủ tịch tô lâm tại hà nội"],
        ["samsung và vingroup ký kết hợp tác tại hà nội"],
        ["bà trần thị bình đại diện vietcombank làm việc tại london"],
        ["câu lạc bộ hà nội fc thi đấu tại sân vận động mỹ đình"],
        # Câu khó - từ đa nghĩa
        ["hà anh tuấn biểu diễn tại đà nẵng và hội an"],
        ["tổng thống joe biden thăm chính thức việt nam"],
        ["vinfast ra mắt xe điện mới tại paris"],
        ["đội tuyển việt nam thi đấu với thái lan tại hà nội"],
        ["google và microsoft hợp tác nghiên cứu trí tuệ nhân tạo"],
    ]
)
if __name__ == "__main__":
    giao_dien.launch()