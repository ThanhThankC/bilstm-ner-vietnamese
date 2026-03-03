# 📘 SỔ TAY LUẬT GÁN NHÃN NER (DÀNH CHO TEAM DATA)

> **Mục tiêu:** Thống nhất 100% cách gán nhãn. Cấm tự suy diễn. Gặp ca khó phải nhắn tin lên group hỏi Leader.

---

## 1. NGUYÊN TẮC CỐT LÕI: Chuẩn BIO

* **`B-` (Begin):** Từ đầu tiên của thực thể.
* **`I-` (Inside):** Các từ nằm bên trong thực thể.
* **`O` (Outside):** Chữ bình thường, không gán gì cả.

> ⚠️ **Luật sinh tử:** Số lượng chữ trong câu phải **BẰNG CHÍNH XÁC** số lượng nhãn. Tuyệt đối không được bỏ sót dấu phẩy, dấu chấm (Các dấu câu này mặc định gán là `O`).

---

## 2. ĐỊNH NGHĨA 3 NHÃN CHÍNH

* **PER (Person - Tên người):** Tên thật, bút danh, nghệ danh của người thật (Việt Nam hoặc nước ngoài).
* **LOC (Location - Địa điểm):** Tên quốc gia, tỉnh, thành, quận, huyện, đường phố, sông, núi, lục địa, châu lục.
* **ORG (Organization - Tổ chức):** Các cơ quan nhà nước, công ty, tập đoàn, trường học, bệnh viện, câu lạc bộ, ban nhạc.

---

## 3. CÁC CA KHÓ "DỄ CÃI NHAU" (BẮT BUỘC NHỚ)

### ❌ Bẫy số 1: Danh xưng và Chức vụ (Không được gán!)
Chỉ gán tên riêng, **tuyệt đối không** bôi đen danh xưng (ông, bà, bác), chức vụ (giám đốc, chủ tịch, giáo sư) hay nghề nghiệp (ca sĩ, cầu thủ).

* **Sai:** `[B-PER: Chủ] [I-PER: tịch] [I-PER: Hồ] [I-PER: Chí] [I-PER: Minh]`
* **Chuẩn:** `[O: Chủ] [O: tịch] [B-PER: Hồ] [I-PER: Chí] [I-PER: Minh]`
* **Chuẩn:** `[O: tỷ] [O: phú] [B-PER: Elon] [I-PER: Musk]`

### ❌ Bẫy số 2: Thực thể lồng nhau (Quy tắc "Gom tất cả")
Khi tên Địa điểm (LOC) nằm bên trong tên Tổ chức (ORG), chúng ta **ưu tiên gán toàn bộ cụm đó thành Tổ chức (ORG)**. Không được cắt vụn ra.

**Ví dụ: "Đại học Quốc gia Hà Nội"**
* **Sai:** `[ORG: Đại học Quốc gia] [LOC: Hà Nội]` *(AI sẽ bị lú)*
* **Chuẩn:** `[B-ORG: Đại] [I-ORG: học] [I-ORG: Quốc] [I-ORG: gia] [I-ORG: Hà] [I-ORG: Nội]`

**Ví dụ: "UBND tỉnh Nghệ An"**
* ➡️ Gán toàn bộ cụm này là **ORG**.

### ❌ Bẫy số 3: Trường học, Bệnh viện, Tòa nhà là LOC hay ORG?
Rất nhiều người nhầm Bệnh viện là một cái nhà (LOC). Trong chuẩn NER quốc tế, Trường học, Bệnh viện, Cơ quan là một nhóm con người được tổ chức lại ➡️ **Phải gán là ORG**.

* **Chuẩn ORG:** Bệnh viện Bạch Mai, Trường THPT Chu Văn An, Tòa án nhân dân.
* **Chuẩn LOC:** Sân vận động Mỹ Đình, Hồ Gươm, ngã tư Hàng Xanh, Vịnh Hạ Long.

### ❌ Bẫy số 4: Từ viết tắt
Vẫn gán bình thường như từ viết đầy đủ. Chỉ cần chú ý xem nó là cái gì.

* **Chuẩn:** `[B-ORG: VFF]` *(Liên đoàn bóng đá).*
* **Chuẩn:** `[B-LOC: TP.HCM]` *(Thành phố Hồ Chí Minh - Chú ý chữ `TP.HCM` nếu viết liền không dấu cách thì nó chỉ là 1 chữ `B-LOC` thôi).*