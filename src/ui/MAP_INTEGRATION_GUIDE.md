# 🗺️ Hướng dẫn tích hợp Map System

## 📋 Tổng quan

Hệ thống bản đồ với các tính năng:
- ✅ Popup hiển thị bản đồ đầy đủ
- ✅ Click vào các tòa nhà để chuyển scene
- ✅ Hiệu ứng hover với tooltip
- ✅ Callback system để xử lý scene transition
- ✅ Dễ dàng thêm tòa nhà mới

## 🏗️ Cấu trúc

```
src/ui/
├── main_scene.py       # UI chính, quản lý các button
├── map_button.py       # MapButton, MapPopup, BuildingButton
└── test_map_button.py  # Demo/Test file
```

## 🎮 Cách sử dụng trong game

### 1. Khởi tạo UI với callback

```python
from src.ui.main_scene import MainSceneUi

def on_building_click(building_id: str):
    """Xử lý khi click vào tòa nhà"""
    if building_id == "office":
        game.change_scene(OfficeScene())
    elif building_id == "toa_thi_chinh":
        game.change_scene(ToaThiChinhScene())

# Khởi tạo UI
ui = MainSceneUi(
    screen_width=1024,
    screen_height=768,
    on_building_click=on_building_click
)
```

### 2. Trong game loop

```python
# Event handling
for event in pygame.event.get():
    # ... xử lý events khác ...
    ui.handle_event(event)

# Update
ui.update()

# Draw
screen.fill((0, 0, 0))
# ... vẽ game objects ...
ui.draw(screen)
```

## 🏢 Thêm tòa nhà mới

### Bước 1: Thêm ảnh vào `assets/images/ui/`
```
assets/images/ui/
├── new-building.png  # Ảnh tòa nhà mới
```

### Bước 2: Cập nhật `map_button.py`

Thêm constant ở đầu file:
```python
NEW_BUILDING_IMG = "assets/images/ui/new-building.png"
```

Thêm button trong `_create_building_buttons()`:
```python
def _create_building_buttons(self, on_click):
    buttons = []
    
    # ... existing buttons ...
    
    # TÒA NHÀ MỚI
    new_building_button = BuildingButton(
        image_path=NEW_BUILDING_IMG,
        position=(300, 400),  # Điều chỉnh vị trí
        scale=0.3,            # Điều chỉnh kích thước
        building_id="new_building",
        on_click=on_click
    )
    buttons.append(new_building_button)
    
    return buttons
```

Thêm tên trong `_draw_tooltip()`:
```python
building_names = {
    "office": "Office Building",
    "toa_thi_chinh": "Tòa Thi Chính",
    "new_building": "Tên Tòa Nhà Mới"  # Thêm dòng này
}
```

### Bước 3: Xử lý trong callback

```python
def on_building_click(building_id: str):
    if building_id == "office":
        game.change_scene(OfficeScene())
    elif building_id == "toa_thi_chinh":
        game.change_scene(ToaThiChinhScene())
    elif building_id == "new_building":  # Thêm xử lý mới
        game.change_scene(NewBuildingScene())
```

## 🎨 Điều chỉnh vị trí và kích thước tòa nhà

### Tìm vị trí phù hợp:

1. Mở bản đồ trong game
2. Xác định vị trí muốn đặt tòa nhà
3. Điều chỉnh `position=(x, y)` trong `BuildingButton`
4. Điều chỉnh `scale` để ảnh vừa vặn

### Tips:
- Vị trí `(0, 0)` là góc trên bên trái của bản đồ
- `scale=1.0` là kích thước gốc, `scale=0.5` là 50% kích thước
- Chạy test file để xem kết quả: `python3 src/ui/test_map_button.py`

## 📊 Thông tin Building IDs hiện tại

| Building ID | Tên hiển thị | Vị trí | Scale |
|-------------|--------------|--------|-------|
| `office` | Office Building | (150, 200) | 0.3 |
| `toa_thi_chinh` | Tòa Thi Chính | (500, 250) | 0.3 |

## 🧪 Testing

Chạy file test:
```bash
cd /home/m1nhph4n/hk251/DA251
python3 src/ui/test_map_button.py
```

Khi click vào tòa nhà, terminal sẽ log:
```
==================================================
🏢 BUILDING CLICKED: office
==================================================
📍 Tên tòa nhà: Office Building
🎯 TODO: Chuyển đến scene của Office Building
==================================================
```

## 🔧 API Reference

### MainSceneUi

```python
MainSceneUi(
    screen_width: int = 800,
    screen_height: int = 600,
    on_building_click: Optional[Callable[[str], None]] = None
)
```

**Methods:**
- `handle_event(event)` - Xử lý pygame events
- `update()` - Cập nhật trạng thái UI
- `draw(screen)` - Vẽ UI lên màn hình
- `set_building_click_handler(handler)` - Thiết lập callback sau khi khởi tạo

### BuildingButton

```python
BuildingButton(
    image_path: str,                              # Đường dẫn ảnh
    position: tuple[int, int],                    # Vị trí (x, y)
    scale: float = 1.0,                          # Tỷ lệ scale
    building_id: str = "",                       # ID duy nhất
    on_click: Optional[Callable[[str], None]] = None  # Callback
)
```

**Properties:**
- `building_id` - ID của tòa nhà
- `is_hovered` - True nếu chuột đang hover
- `rect` - pygame.Rect cho collision detection

## 🎯 TODO List

- [ ] Tạo các scene classes cho từng tòa nhà
- [ ] Implement scene manager/game state manager
- [ ] Thêm animation khi hover/click
- [ ] Thêm sound effects
- [ ] Tối ưu vị trí và scale các tòa nhà trên bản đồ
- [ ] Thêm nhiều tòa nhà hơn

## 💡 Tips & Best Practices

1. **Vị trí tòa nhà**: Điều chỉnh trong `_create_building_buttons()` cho chính xác
2. **Callback pattern**: Sử dụng callback để tách biệt UI logic và game logic
3. **Testing**: Luôn test với file test trước khi tích hợp vào game chính
4. **Performance**: BuildingButtons chỉ update khi popup mở, tối ưu performance

## 🐛 Troubleshooting

**Problem**: Ảnh tòa nhà không hiển thị
- ✅ Kiểm tra đường dẫn file
- ✅ Kiểm tra scale (có thể quá nhỏ hoặc quá lớn)
- ✅ Kiểm tra position (có thể nằm ngoài popup)

**Problem**: Click không hoạt động
- ✅ Đảm bảo gọi `ui.handle_event(event)` trong event loop
- ✅ Đảm bảo gọi `ui.update()` trong game loop
- ✅ Kiểm tra callback đã được set chưa

**Problem**: Tooltip không hiển thị đúng tên
- ✅ Thêm building_id vào dict `building_names` trong `_draw_tooltip()`
