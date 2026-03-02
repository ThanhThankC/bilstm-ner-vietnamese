import gradio as gr
from transformers import pipeline

print("Đang tải mô hình AI tiếng Việt (lần đầu sẽ hơi lâu để tải về máy)...")
# Tải mô hình NER tiếng Việt đã được huấn luyện sẵn (Pre-trained)
ner_model = pipeline("ner", model="NlpHUST/ner-vietnamese-electra-base", aggregation_strategy="simple")
print("Tải xong! Đang khởi động giao diện...")

# Hàm xử lý: Nhận input là text, output là danh sách các từ và nhãn
def nhan_dien_thuc_the(van_ban):
    # Đưa văn bản vào mô hình dự đoán
    ket_qua = ner_model(van_ban)
    
    # Định dạng lại kết quả để hiển thị đẹp trên Web
    hien_thi = []
    vi_tri_cu = 0
    
    for thuc_the in ket_qua:
        tu = thuc_the['word']
        nhan = thuc_the['entity_group']
        bat_dau = thuc_the['start']
        ket_thuc = thuc_the['end']
        
        # Thêm phần chữ bình thường (không phải thực thể) vào danh sách
        hien_thi.append((van_ban[vi_tri_cu:bat_dau], None))
        # Thêm phần thực thể và nhãn của nó vào danh sách
        hien_thi.append((van_ban[bat_dau:ket_thuc], nhan))
        
        vi_tri_cu = ket_thuc
        
    # Thêm phần chữ còn sót lại ở cuối câu
    hien_thi.append((van_ban[vi_tri_cu:], None))
    
    return hien_thi

# Xây dựng giao diện Web UI với Gradio
giao_dien = gr.Interface(
    fn=nhan_dien_thuc_the, # Hàm xử lý gọi ở trên
    inputs=gr.Textbox(lines=4, placeholder="Nhập câu tiếng Việt vào đây...", label="Văn bản đầu vào (Input)"),
    outputs=gr.HighlightedText(label="Kết quả nhận diện (Output)"),
    title="Hệ thống Nhận diện Thực thể (NER) - Nhóm của tôi",
    description="Hệ thống tự động nhận diện Tên người (PER), Địa điểm (LOC) và Tổ chức (ORG) trong văn bản tiếng Việt.",
    examples=[
        ["Ông Phạm Nhật Vượng là người sáng lập tập đoàn Vingroup, có trụ sở tại thủ đô Hà Nội."],
        ["Trường Đại học Bách Khoa Hà Nội nằm ở đường Đại Cồ Việt."]
    ] # Cung cấp sẵn vài câu ví dụ để cô giáo bấm thử
)

# Chạy ứng dụng
if __name__ == "__main__":
    giao_dien.launch()