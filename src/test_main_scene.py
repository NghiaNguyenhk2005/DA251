import pygame
from pygame.event import get

from scenes.office import OfficeScene
from ui import MainSceneUi
from scenes import *
from interfaces import DrawAndUpdateAble

def main():
    # Khởi tạo pygame
    pygame.init()
    
    # Thiết lập màn hình
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test Map Button - Click vào tòa nhà để xem")
    
    # Tạo clock để kiểm soát FPS
    clock = pygame.time.Clock()

    # Init Scenes
    scene_dict: dict = {
        "office": OfficeScene(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT),
        "interrogation_room": InterrogationRoomScene(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT),
    }
    cur_scene:DrawAndUpdateAble = scene_dict["interrogation_room"]

    def change_scene(building_id: str):
        nonlocal cur_scene
        print(f"\n✨ Scene changed to: {building_id}\n")
        cur_scene = scene_dict.get(building_id, scene_dict["office"])

    # Khởi tạo UI với callback handler
    ui = MainSceneUi(
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        on_building_click=change_scene
    )
    
    # In hướng dẫn
    print("\n" + "="*60)
    print("🎮 MAP BUTTON TEST - HƯỚNG DẪN SỬ DỤNG")
    print("="*60)
    print("1. Click vào nút MAP để mở bản đồ")
    print("2. Hover chuột vào các tòa nhà để xem tên")
    print("3. Click vào tòa nhà để 'chuyển scene' (hiện tại chỉ log)")
    print("4. Click nút X hoặc bên ngoài popup để đóng")
    print("5. Nhấn ESC để thoát")
    print("="*60 + "\n")
    
    # Game loop
    running = True
    while running:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # Xử lý sự kiện cho UI
            ui.handle_event(event)
        
        # Cập nhật
        cur_scene.update()
        ui.update()

        # Vẽ
        screen.fill((200, 200, 200))  # Background màu xám nhạt
        
        # Draw cur.scene
        cur_scene.draw(screen=screen)

        # Vẽ UI
        ui.draw(screen)
        
        # Cập nhật màn hình
        pygame.display.flip()
        
        # Giới hạn FPS
        clock.tick(60)
    
    pygame.quit()
    print("\n👋 Thoát chương trình\n")

if __name__ == "__main__":
    main()
