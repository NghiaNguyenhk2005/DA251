# 📚 DA251 Project - Refactor Guide

## 🏗️ Cấu trúc hiện tại

```
src/
├── interfaces/          # Protocol patterns (Drawable, Updatable, DrawAndUpdateAble)
├── ui/                  # UI components (Button, TextButton, MenuPopup, MainSceneUi)
├── scenes/              # Game scenes (OfficeScene, InterrogationRoomScene)
└── test_main_scene.py   # Main test file
```

---

## 📦 Interfaces (`src/interfaces/`)

### Các Protocol chính:
- **`Drawable`**: Có method `draw(screen: pygame.Surface)`
- **`Updatable`**: Có method `update(delta_time)` và `handle_event(event)`
- **`DrawAndUpdateAble`**: Kết hợp cả 2 trên

### Export từ `__init__.py`:
```python
from .draw_and_update import Drawable, Updatable, DrawAndUpdateAble
```

---

## 🎨 UI Components (`src/ui/`)

### Button System (`button.py`)

**`IButton`** (Interface):
- `was_clicked() -> bool`
- `is_pressed() -> bool`

**`Button`** (Sprite-based):
- Dùng sprite sheet cho các state (normal/hover/clicked)
- Params: `position`, `image`, `scale`, `split`

**`TextButton`** (Text-based):
- Button dạng text + background màu
- **Có rounded corners** với `border_radius` (default: 10)
- Params: `position`, `text`, `font_size`, `padding`, colors cho 3 states, `border_radius`

### MenuPopup (`menu_popup.py`)
- 3 TextButtons: Resume, Settings, Quit
- Methods: `toggle()`, `is_open()`, `update()`, `draw()`
- **Gray theme hiện tại**: 
  - Resume: (70, 70, 70)
  - Settings: (85, 85, 85)
  - Quit: (100, 100, 100)

### MainSceneUi (`main_scenes.py`)
- Quản lý: `menu_button`, `map_button`, `journal_button`, `menu_popup`
- Update và vẽ tất cả UI components

### Export từ `__init__.py`:
```python
from .button import IButton, Button, TextButton
from .main_scenes import MainSceneUi
from .tooltip import Tooltip
```

---

## 🧪 Test Main Scene (`test_main_scene.py`)

### Flow chính:
1. Init pygame + screen + clock
2. Tạo `scene_dict` với các scenes
3. Tạo `MainSceneUi`
4. Game loop:
   - Handle events → `ui.handle_event()`
   - Update → `cur_scene.update()` + `ui.update()`
   - Check scene switching qua map button clicks
   - Draw → `cur_scene.draw()` + `ui.draw()`

---

## 💡 Gợi ý Refactor (ngắn gọn)

### 1. Scene Manager
Tạo class `SceneManager` để quản lý scenes thay vì `scene_dict`:
```python
scene_manager.register_scene("office", OfficeScene(...))
scene_manager.switch_to("office")
```

### 2. Event Handler
Tạo class `EventHandler` để xử lý events tập trung:
```python
event_handler.register_handler(ui)
event_handler.process_events()
```

### 3. UI State Manager
Thêm method `get_scene_change_request()` vào `MainSceneUi` thay vì check trong game loop.

### 4. Config Manager
Tách constants (colors, paths, settings) ra `config.py`.

### 5. Game Wrapper
Đóng gói tất cả vào class `Game` với method `run()`.

---

## ⚠️ Lưu ý quan trọng

### ✅ Giữ nguyên:
- Interfaces (Drawable, Updatable, DrawAndUpdateAble)
- Button, TextButton API
- Game logic hiện tại

### 🔧 Best Practices:
- Dùng type hints
- Mỗi class một trách nhiệm (Single Responsibility)
- Keep game loop simple
- Tách logic ra khỏi main loop

### 🎨 Gray Theme Colors:
```python
# Buttons (normal → hover → click)
PRIMARY = (70, 70, 70) → (120, 120, 120) → (50, 50, 50)
SECONDARY = (85, 85, 85) → (135, 135, 135) → (65, 65, 65)
TERTIARY = (100, 100, 100) → (150, 150, 150) → (80, 80, 80)

# UI Elements
BORDER = (200, 200, 200)
TEXT = (255, 255, 255)
BACKGROUND = (200, 200, 200)
```

---

**Version**: 1.0 | **Project**: DA251 - Detective Game
