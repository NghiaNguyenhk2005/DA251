# 🗺️ MAP SYSTEM - BUILDING CLICK FEATURE

## ✅ ĐÃ HOÀN THÀNH

### 📦 Files đã tạo/cập nhật:

1. **`src/ui/map_button.py`** ⭐ MAIN FILE
   - `BuildingButton` class - Quản lý từng tòa nhà trên bản đồ
   - `MapPopup` class - Popup hiển thị bản đồ với các tòa nhà
   - `MapButton` class - Button mở/đóng popup
   - Tích hợp callback system

2. **`src/ui/main_scene.py`** ⭐ UPDATED
   - Tích hợp callback cho building clicks
   - Hỗ trợ custom handler hoặc default handler

3. **`src/ui/test_map_button.py`** 🧪 TEST FILE
   - Demo đầy đủ chức năng
   - In log khi click vào tòa nhà

4. **`src/ui/example_scene_manager.py`** 📚 EXAMPLE
   - Demo cách tích hợp với scene manager
   - Có sẵn 3 scenes: Main, Office, Tòa Thi Chính
   - Chuyển scene khi click tòa nhà

5. **`src/ui/MAP_INTEGRATION_GUIDE.md`** 📖 DOCUMENTATION
   - Hướng dẫn chi tiết cách sử dụng
   - Hướng dẫn thêm tòa nhà mới
   - API reference đầy đủ

---

## 🎯 TÍNH NĂNG

### ✨ Hiện có:
- ✅ Click vào tòa nhà để trigger callback
- ✅ Hiệu ứng hover với viền vàng sáng
- ✅ Tooltip hiển thị tên tòa nhà khi hover
- ✅ Callback system để xử lý scene transition
- ✅ 2 tòa nhà đã được tích hợp:
  - 🏢 Office Building (building_id: "office")
  - 🏛️ Tòa Thi Chính (building_id: "toa_thi_chinh")

### 🎨 Hiệu ứng UI:
- Overlay vàng nhạt khi hover
- Viền vàng sáng khi hover
- Tooltip với tên tòa nhà
- Smooth interaction

---

## 🚀 CÁCH SỬ DỤNG

### 1️⃣ Test đơn giản (chỉ log):
```bash
python3 src/ui/test_map_button.py
```

### 2️⃣ Demo với Scene Manager:
```bash
python3 src/ui/example_scene_manager.py
```
Trong demo này:
- Click Map button → Mở bản đồ
- Click Office Building → Chuyển sang Office Scene
- Click Tòa Thi Chính → Chuyển sang Tòa Thi Chính Scene
- Nhấn BACKSPACE → Quay lại Main Scene

### 3️⃣ Tích hợp vào game của bạn:

```python
from src.ui.main_scene import MainSceneUi

def handle_building_click(building_id: str):
    """Callback khi click tòa nhà"""
    if building_id == "office":
        game.change_scene("office")  # Code của bạn
    elif building_id == "toa_thi_chinh":
        game.change_scene("toa_thi_chinh")  # Code của bạn

# Khởi tạo UI
ui = MainSceneUi(
    screen_width=1024,
    screen_height=768,
    on_building_click=handle_building_click  # Truyền callback
)

# Trong game loop:
for event in pygame.event.get():
    ui.handle_event(event)

ui.update()
ui.draw(screen)
```

---

## 🏢 BUILDING CONFIGURATION

### Hiện tại:
| Building ID | Image File | Position | Scale | Tên hiển thị |
|------------|------------|----------|-------|--------------|
| `office` | `office-map-scene.png` | (150, 200) | 0.3 | Office Building |
| `toa_thi_chinh` | `toa-chi-chinh.png` | (500, 250) | 0.3 | Tòa Thi Chính |

### ⚠️ TODO: Điều chỉnh vị trí & scale

Vị trí và scale hiện tại là **placeholder**. Bạn cần:
1. Chạy test file
2. Mở bản đồ
3. Xem các tòa nhà có nằm đúng vị trí không
4. Điều chỉnh trong `map_button.py` → `_create_building_buttons()`

```python
# Trong map_button.py, method _create_building_buttons():
office_button = BuildingButton(
    image_path=OFFICE_MAP_SCENE_IMG,
    position=(150, 200),  # ← ĐIỀU CHỈNH TẠI ĐÂY
    scale=0.3,            # ← ĐIỀU CHỈNH TẠI ĐÂY
    building_id="office",
    on_click=on_click
)
```

---

## ➕ THÊM TÒA NHÀ MỚI

### Bước 1: Thêm ảnh
```
assets/images/ui/new-building.png
```

### Bước 2: Thêm constant (đầu file `map_button.py`)
```python
NEW_BUILDING_IMG = "assets/images/ui/new-building.png"
```

### Bước 3: Thêm button (trong `_create_building_buttons()`)
```python
new_building_button = BuildingButton(
    image_path=NEW_BUILDING_IMG,
    position=(400, 300),  # Vị trí trên bản đồ
    scale=0.3,
    building_id="new_building",
    on_click=on_click
)
buttons.append(new_building_button)
```

### Bước 4: Thêm tên tooltip (trong `_draw_tooltip()`)
```python
building_names = {
    "office": "Office Building",
    "toa_thi_chinh": "Tòa Thi Chính",
    "new_building": "Tên Tòa Mới"  # ← Thêm
}
```

### Bước 5: Xử lý trong callback
```python
def handle_building_click(building_id: str):
    if building_id == "office":
        # ...
    elif building_id == "new_building":  # ← Thêm
        game.change_scene("new_building")
```

---

## 📝 NOTES

### Assets đã sử dụng:
- ✅ `assets/images/ui/map_scene.png` - Bản đồ nền
- ✅ `assets/images/ui/office-map-scene.png` - Icon Office
- ✅ `assets/images/ui/toa-chi-chinh.png` - Icon Tòa Thi Chính
- ✅ `assets/images/ui/map-button.png` - Button mở bản đồ

### Callback System:
- Callback nhận parameter: `building_id: str`
- Building ID là unique identifier cho từng tòa nhà
- Sử dụng để xác định scene nào cần load

### Performance:
- BuildingButtons chỉ update khi popup đang mở
- Collision detection chỉ chạy khi popup visible
- Tối ưu cho nhiều tòa nhà

---

## 🔧 TROUBLESHOOTING

### Lỗi: ModuleNotFoundError: No module named 'pygame'
```bash
pip install pygame
# hoặc
pip3 install pygame
```

### Lỗi: Không thấy tòa nhà trên bản đồ
- Kiểm tra đường dẫn file ảnh
- Kiểm tra scale (có thể quá nhỏ)
- Kiểm tra position (có thể nằm ngoài popup)

### Lỗi: Click không hoạt động
- Đảm bảo gọi `ui.handle_event(event)`
- Đảm bảo gọi `ui.update()`
- Kiểm tra callback đã set chưa

### Tooltip hiển thị sai tên
- Thêm building_id vào `building_names` dict trong `_draw_tooltip()`

---

## 📚 XEM THÊM

- `MAP_INTEGRATION_GUIDE.md` - Hướng dẫn chi tiết
- `example_scene_manager.py` - Demo đầy đủ với scene manager
- `test_map_button.py` - Test cơ bản

---

## 🎉 KẾT LUẬN

Hệ thống đã sẵn sàng sử dụng! 

**Việc cần làm tiếp:**
1. Cài pygame nếu chưa có
2. Chạy test để xem kết quả
3. Điều chỉnh vị trí & scale các tòa nhà
4. Implement các scene tương ứng
5. Tích hợp vào game chính

**Liên hệ/Câu hỏi:**
- Đọc `MAP_INTEGRATION_GUIDE.md` để biết thêm chi tiết
- Chạy `example_scene_manager.py` để xem demo đầy đủ

Good luck! 🚀
