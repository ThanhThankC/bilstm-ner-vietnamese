import json
import sys
import os

def main():
    # 1. Kiểm tra xem người dùng đã truyền tên file đầu ra chưa
    if len(sys.argv) < 2:
        print("Lỗi: Thiếu file đầu ra!")
        print("Cách sử dụng: python format/trans_format.py <đường_dẫn_file_đầu_ra>")
        print("Ví dụ: python format/trans_format.py data/dataset_A.json")
        sys.exit(1)

    # Lấy đường dẫn file đầu ra từ dòng lệnh 
    output_file = sys.argv[1]
    
    # 2. Xác định đường dẫn file đầu vào cố định (format/dataset.json)
    # Dùng os.path để code luôn chạy đúng dù bạn gọi lệnh từ thư mục nào
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "dataset.json")

    # 3. Đọc dữ liệu từ file đầu vào
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file đầu vào tại '{input_file}'")
        print("Hãy chắc chắn A đã export file vào đúng thư mục format/ nhé.")
        sys.exit(1)

    # 4. Xử lý định dạng
    formatted_items = []
    for item in data:
        tokens_str = json.dumps(item.get("tokens", []), ensure_ascii=False)
        labels_str = json.dumps(item.get("labels", []), ensure_ascii=False)
        
        obj_str = f'  {{\n    "tokens": {tokens_str},\n    "labels": {labels_str}\n  }}'
        formatted_items.append(obj_str)

    final_json = "[\n" + ",\n".join(formatted_items) + "\n]"

    # 5. Lưu ra file đích
    # Tạo thư mục 'data/' nếu nó chưa tồn tại để tránh lỗi
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_json)
    
    print(f"✅ Xong! Đã định dạng và lưu file tại: {output_file}")

if __name__ == "__main__":
    main()