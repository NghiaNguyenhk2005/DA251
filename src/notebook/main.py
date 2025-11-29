# file: main.py
import pygame
from .notebook import Notebook
from .clues_data import clues 

# --- Hằng số Cài đặt Game ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Cấu hình biểu tượng sổ khi đóng
CLOSED_BOOK_ICON_SIZE = (64, 64) # Kích thước biểu tượng
CLOSED_BOOK_ICON_POS = (SCREEN_WIDTH - CLOSED_BOOK_ICON_SIZE[0] - 20, 20) # Góc phải trên màn hình

def load_fonts():
    """Tải tất cả các font và trả về dưới dạng một dictionary."""
    fonts = {}
    try:
        fonts['list'] = pygame.font.Font("src/assets/fonts/Harmonic.ttf", 36)
        
        font_title_sizes = [42, 36, 32, 28, 24]

        fonts['title_options'] = {size: pygame.font.Font("src/assets/fonts/Harmonic.ttf", size) for size in font_title_sizes}
        
        font_desc_sizes = [36, 32, 28, 24]
        # === SỬA LỖI TẠI ĐÂY ===
        # Phải dùng "Harmonic.ttf" cho description
        fonts['desc_options'] = {size: pygame.font.Font("src/assets/fonts/Harmonic.ttf", size) for size in font_desc_sizes}
        
        fonts['page_count'] = pygame.font.Font("src/assets/fonts/Harmonic.ttf", 28)
        
    except FileNotFoundError:
        print("Warning: 'Harmonic.ttf' not found. Using default font.")
        fonts['list'] = pygame.font.Font(None, 40)
        
        font_title_sizes = [42, 36, 32, 28, 24]
        fonts['title_options'] = {size: pygame.font.Font(None, size + 4) for size in font_title_sizes}
        
        font_desc_sizes = [36, 32, 28, 24]
        fonts['desc_options'] = {size: pygame.font.Font(None, size + 4) for size in font_desc_sizes}
        
        fonts['page_count'] = pygame.font.Font(None, 32)
        
    return fonts

def load_images():
    """Tải hình ảnh và trả về dưới dạng dictionary."""
    images = {}

    images['closed_book_icon'] = pygame.image.load("src/assets/notebook/brownbook.png").convert_alpha()
    images['closed_book_icon'] = pygame.transform.scale(images['closed_book_icon'], CLOSED_BOOK_ICON_SIZE)

    return images

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Detective's Notebook")
    clock = pygame.time.Clock()

    all_fonts = load_fonts()
    all_images = load_images() # Tải hình ảnh

    game_notebook = Notebook(
        screen=screen, 
        clock=clock, 
        clues_data=clues, 
        fonts=all_fonts,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT
    )

    # Rect cho icon sổ nhỏ
    closed_book_icon_rect = pygame.Rect(CLOSED_BOOK_ICON_POS, CLOSED_BOOK_ICON_SIZE)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Xử lý sự kiện chung hoặc cho sổ đang đóng
            if not game_notebook.get_state(): # Nếu sổ đang đóng
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if closed_book_icon_rect.collidepoint(mouse_pos):
                        game_notebook.open_notebook()
            else: # Nếu sổ đang mở, chuyển sự kiện cho Notebook xử lý
                game_notebook.handle_event(event, mouse_pos)

        # Cập nhật logic (chỉ cho Notebook nếu nó đang mở)
        game_notebook.update()

        # Vẽ
        screen.fill((0, 0, 0)) # Xóa màn hình với màu đen hoặc nền game chính

        if game_notebook.get_state(): # Nếu sổ đang mở, vẽ cuốn sổ
            game_notebook.draw(mouse_pos)
        else: # Nếu sổ đang đóng, vẽ biểu tượng sổ nhỏ
            screen.blit(all_images['closed_book_icon'], closed_book_icon_rect)
            # Có thể thêm hiệu ứng hover cho icon sổ nhỏ tại đây nếu muốn
            if closed_book_icon_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), closed_book_icon_rect, 2) # Viền trắng khi hover

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()