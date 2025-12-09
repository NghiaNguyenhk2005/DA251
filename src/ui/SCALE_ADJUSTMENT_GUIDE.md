# 🔧 HƯỚNG DẪN ĐIỀU CHỈNH SCALE TÒA NHÀ

## ❓ Vấn đề: Scale không thay đổi?

### Nguyên nhân có thể:
1. ❌ Chưa restart chương trình sau khi sửa code
2. ❌ Ảnh gốc quá lớn, scale 0.3 vẫn to
3. ❌ Code bị cache, Python dùng file .pyc cũ
4. ❌ Sửa sai file hoặc sai vị trí

---

## ✅ GIẢI PHÁP

### Cách 1: Dùng Interactive Tool (RECOMMENDED) 🌟

```bash
python3 src/ui/scale_adjuster.py
```

**Hướng dẫn:**
1. Click nút MAP để mở bản đồ
2. Dùng phím điều chỉnh:
   - `TAB` - Chuyển giữa Office và Tòa Thi Chính
   - `Arrow Keys` (↑↓←→) - Di chuyển vị trí
   - `+/-` - Tăng/giảm scale
   - `P` - In ra code để copy
3. Nhấn `P` khi hài lòng
4. Copy code vào `map_button.py`

**Ưu điểm:** Thấy ngay kết quả, không cần restart!

---

### Cách 2: Sửa trực tiếp trong map_button.py

**File:** `/home/m1nhph4n/hk251/DA251/src/ui/map_button.py`

**Tìm method:** `_create_building_buttons()`

**Sửa tại đây:**
```python
def _create_building_buttons(self, on_click):
    buttons = []
    
    # OFFICE BUILDING
    office_button = BuildingButton(
        image_path=OFFICE_MAP_SCENE_IMG,
        position=(150, 200),  # ⬅️ ĐIỀU CHỈNH X, Y
        scale=0.15,           # ⬅️ ĐIỀU CHỈNH SCALE (0.1 = 10%)
        building_id="office",
        on_click=on_click
    )
    buttons.append(office_button)
    
    # TÒA THI CHÍNH
    toa_thi_chinh_button = BuildingButton(
        image_path=TOA_THI_CHINH_IMG,
        position=(500, 250),  # ⬅️ ĐIỀU CHỈNH X, Y
        scale=0.15,           # ⬅️ ĐIỀU CHỈNH SCALE (0.1 = 10%)
        building_id="toa_thi_chinh",
        on_click=on_click
    )
    buttons.append(toa_thi_chinh_button)
    
    return buttons
```

**Sau khi sửa:**
1. Save file
2. **Tắt hoàn toàn** chương trình đang chạy
3. Chạy lại: `python3 src/ui/test_map_button.py`

---

### Cách 3: Xoá cache và restart

```bash
# Xoá tất cả file cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete

# Chạy lại
python3 src/ui/test_map_button.py
```

---

## 📊 SCALE REFERENCE

| Scale | Ý nghĩa | Khi nào dùng |
|-------|---------|--------------|
| 0.05 | 5% kích thước gốc | Ảnh cực lớn, chỉ cần icon nhỏ |
| 0.1 | 10% | Ảnh rất lớn |
| 0.15 | 15% | **Mặc định hiện tại** |
| 0.2 | 20% | Ảnh lớn |
| 0.3 | 30% | Ảnh trung bình |
| 0.5 | 50% | Giảm một nửa |
| 1.0 | 100% (gốc) | Giữ nguyên kích thước |
| 2.0 | 200% | Phóng to gấp đôi |

---

## 🐛 DEBUG - Kiểm tra kích thước ảnh

Khi chạy test file, bây giờ sẽ in ra:

```
[MapPopup] Office button created - Original: (1200, 800), Scaled: (180, 120)
[MapPopup] Tòa Thi Chính button created - Original: (1000, 900), Scaled: (150, 135)
```

**Giải thích:**
- `Original` - Kích thước ảnh gốc
- `Scaled` - Kích thước sau khi scale

**Ví dụ:** Nếu ảnh gốc `1200x800` với scale `0.15`:
- Scaled width = 1200 × 0.15 = 180px
- Scaled height = 800 × 0.15 = 120px

---

## 💡 TIPS

### Ảnh vẫn quá lớn?
- Giảm scale xuống 0.1 hoặc 0.05
- Hoặc resize ảnh gốc bằng tool khác

### Ảnh quá nhỏ?
- Tăng scale lên 0.3, 0.5, hoặc cao hơn
- Kiểm tra ảnh gốc có đủ resolution không

### Kiểm tra nhanh kích thước ảnh gốc:
```bash
# Dùng ImageMagick
identify assets/images/ui/office-map-scene.png
identify assets/images/ui/toa-chi-chinh.png

# Hoặc Python
python3 -c "import pygame; pygame.init(); img = pygame.image.load('assets/images/ui/office-map-scene.png'); print(f'Size: {img.get_size()}')"
```

---

## ✨ RECOMMENDED WORKFLOW

1. **Chạy Scale Adjuster:**
   ```bash
   python3 src/ui/scale_adjuster.py
   ```

2. **Điều chỉnh trực quan:**
   - Mở bản đồ
   - Dùng phím điều chỉnh
   - Xem ngay kết quả

3. **In code:**
   - Nhấn `P` khi hài lòng
   - Terminal sẽ in code

4. **Copy vào map_button.py:**
   - Copy code từ terminal
   - Paste vào method `_create_building_buttons()`

5. **Test:**
   ```bash
   python3 src/ui/test_map_button.py
   ```

---

## 🎯 KẾT LUẬN

**Vấn đề hiện tại:** Scale đã giảm từ 0.3 xuống 0.15 và có debug log

**Nếu vẫn không đổi:**
1. Dùng `scale_adjuster.py` để điều chỉnh trực quan
2. Hoặc restart hoàn toàn terminal và chạy lại
3. Hoặc xoá cache Python

**Nếu cần hỗ trợ thêm:**
- Chạy `scale_adjuster.py` và gửi screenshot
- Hoặc in ra: `identify assets/images/ui/*.png`
