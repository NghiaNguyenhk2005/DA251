# file: notebook.py
import pygame
import math

# --- Hằng số & Cài đặt (Giữ nguyên) ---
COLOR_DARK_COVER = (25, 25, 30)
COLOR_BOOK_COVER = (150, 75, 0)
COLOR_BOOK_BORDER_BROWN = (100, 50, 0)
COLOR_BOOK_HIGHLIGHT = (180, 105, 30)
COLOR_BOOK_INNER = (240, 220, 180)
COLOR_PAGE_SHADOW = (210, 190, 150)
COLOR_LINE = (120, 80, 50) # Vẫn cần màu này
COLOR_BORDER = (0, 0, 0)
COLOR_SPINE_METAL = (150, 150, 150)
COLOR_SPINE_HIGHLIGHT = (210, 210, 210)
COLOR_SPINE_SHADOW = (90, 90, 90)
COLOR_SPINE_HOLE = (50, 50, 50)
COLOR_RIBBON = (0, 100, 150)
COLOR_SELECT_LINE = (200, 0, 0)
COLOR_BUTTON_TEXT = (10, 10, 10)
COLOR_BUTTON_HOVER = (0, 100, 200)
COLOR_TEXT_BRIGHT = (10, 10, 10)
COLOR_TEXT_DIM = (194, 178, 146)
COLOR_CLOSE_BUTTON = (200, 50, 50) 
COLOR_CLOSE_BUTTON_HOVER = (255, 0, 0) 

# --- Cài đặt ---
PULSE_CYCLE_MS = 1000.0
PULSE_HALF_CYCLE = PULSE_CYCLE_MS / 2.0
CLUES_PER_PAGE = 10
LINE_SPACING = 50 # <<< THAY ĐỔI: Điều chỉnh khoảng cách dòng (từ 52)
FIRST_LINE_OFFSET_Y = -30 # <<< THAY ĐỔI: Tăng lề trên (từ 30)
TEXT_ABOVE_LINE_OFFSET = 5 # <<< THÊM MỚI: Pixel để đẩy chữ lên trên dòng kẻ


# --- Hàm trợ giúp (Giữ nguyên) ---
def draw_text(surface, text, font, color, rect, aa=True, bkg=None, line_height_override=None):
    y = rect.top
    actual_line_step = line_height_override if line_height_override is not None else font.get_linesize()
    original_rect_bottom = rect.bottom
    while text and y <= original_rect_bottom:
        i = 1
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text):
            temp_i = text.rfind(" ", 0, i)
            if temp_i != -1 and temp_i != 0:
                i = temp_i + 1
            elif i == 0:
                i = 1
        # Nên dùng aa=False nếu bạn đổi sang font pixel
        image = font.render(text[:i], aa, color, bkg)
        image_rect = image.get_rect(bottomleft=(rect.left, y))
        surface.blit(image, image_rect)
        y += actual_line_step
        text = text[i:]
    return text

def get_sprite(sheet, x, y, width, height):
    """Hàm này cắt 1 sprite từ spritesheet."""
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

def lerp_color(color_a, color_b, t):
    r = color_a[0] + (color_b[0] - color_a[0]) * t
    g = color_a[1] + (color_b[1] - color_a[1]) * t
    b = color_a[2] + (color_b[2] - color_a[2]) * t
    return (int(r), int(g), int(b))

def check_text_fit(text, font, rect_width, max_lines, line_height_override=None):
    line_count = 0
    while text:
        line_count += 1
        if line_count > max_lines:
            return False
        i = 1
        while font.size(text[:i])[0] < rect_width and i < len(text):
            i += 1
        if i < len(text):
            temp_i = text.rfind(" ", 0, i)
            if temp_i != -1 and temp_i != 0:
                i = temp_i + 1
            elif i == 0:
                i = 1
        text = text[i:]
    return True


# --- Lớp Sổ Tay Chính ---
class Notebook:
    def __init__(self, screen, clock, clues_data, fonts, screen_width, screen_height):
        self.screen = screen
        self.clock = clock
        self.clues = clues_data
        self.fonts = fonts
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.selected_clue_index = -1
        self.clue_list_rects = []
        self.current_page = 0
        self.total_pages = 1
        self.running = False
        self.current_pulse_color = COLOR_TEXT_BRIGHT
        self.is_open = False

        # Tải asset tại đây
        try:
            self.ui_spritesheet = pygame.image.load("src/assets/notebook/bookassets.png").convert_alpha()
        except pygame.error as e:
            print(f"LỖI: Không tải được 'bookassets.png': {e}")
            self.ui_spritesheet = pygame.Surface((1,1), pygame.SRCALPHA)

        # === SỬA TỌA ĐỘ TẠI ĐÂY ===
        # Cắt sprite gốc (chưa scale)
        # Dùng sprite (16, 208, 111, 80) KHÔNG có dòng kẻ
        self.notebook_bg_sprite_original = get_sprite(self.ui_spritesheet, 16, 176, 95, 48)
        
        # Sprite đã scale (sẽ được gán trong _calculate_layout)
        self.notebook_background_sprite = None 
        
        self._calculate_layout()

    def _calculate_layout(self):
        # Kích thước mong muốn trên màn hình (Giữ nguyên)
        BOOK_TOTAL_WIDTH = 800
        BOOK_TOTAL_HEIGHT = 600
        
        # Tính toán vị trí sổ
        self.BOOK_X = (self.screen_width - BOOK_TOTAL_WIDTH) // 2 
        self.BOOK_Y = (self.screen_height - BOOK_TOTAL_HEIGHT) // 2
        
        # Tỉ lệ scale (bị co giãn, nhưng giữ kích thước 800x600)
        scale_x = BOOK_TOTAL_WIDTH / self.notebook_bg_sprite_original.get_width() 
        scale_y = BOOK_TOTAL_HEIGHT / self.notebook_bg_sprite_original.get_height()
        
        # Tọa độ bên trong sprite (111x80)
        SPRITE_LEFT_PAGE_X = 8      # Lề trái của trang trái
        SPRITE_LEFT_PAGE_W = 40     # Chiều rộng trang trái
        SPRITE_RIGHT_PAGE_X = 63    # Lề trái của trang phải
        SPRITE_RIGHT_PAGE_W = 40    # Chiều rộng trang phải
        SPRITE_PAGE_TOP_Y = 8       # Lề trên của cả 2 trang
        
        TEXT_PADDING = 20 # Lề 20px bên trong vùng giấy
        
                # --- Tính toán Vùng Text Trang Trái ---
        self.CLUE_LIST_AREA_X = self.BOOK_X + (SPRITE_LEFT_PAGE_X * scale_x) + TEXT_PADDING
        self.CLUE_LIST_AREA_Y = self.BOOK_Y + (SPRITE_PAGE_TOP_Y * scale_y)
        self.CLUE_LIST_AREA_WIDTH = (SPRITE_LEFT_PAGE_W * scale_x) - (2 * TEXT_PADDING)
        
        # --- Tính toán Vùng Text Trang Phải ---
        self.INFO_DETAIL_AREA_X = self.BOOK_X + (SPRITE_RIGHT_PAGE_X * scale_x) + TEXT_PADDING
        self.INFO_DETAIL_AREA_Y = self.BOOK_Y + (SPRITE_PAGE_TOP_Y * scale_y)
        self.INFO_DETAIL_AREA_WIDTH = (SPRITE_RIGHT_PAGE_W * scale_x) - (2 * TEXT_PADDING)

        # <<< DỊCH TRÁI TOÀN BỘ VÙNG CHỮ  >>>
        SHIFT_LEFT = 45
        self.CLUE_LIST_AREA_X -= SHIFT_LEFT
        self.INFO_DETAIL_AREA_X -= 80

        
        # --- Tính toán Nút bấm (Căn chỉnh lại) ---
        page_turn_y_pos = self.BOOK_Y + BOOK_TOTAL_HEIGHT - 55 # Căn y vào vị trí mới
        self.page_count_y = self.BOOK_Y + BOOK_TOTAL_HEIGHT - 40
        
        ARROW_SIZE_W = 15
        ARROW_SIZE_H = 20
        
        # Nút trang trước (Căn vào trang trái)
        self.prev_page_rect = pygame.Rect(self.CLUE_LIST_AREA_X, 
                                          page_turn_y_pos - (ARROW_SIZE_H // 2), 
                                          ARROW_SIZE_W, ARROW_SIZE_H)
        
        # Nút trang sau (Căn vào trang phải)
        next_page_x_pos = self.INFO_DETAIL_AREA_X + self.INFO_DETAIL_AREA_WIDTH - ARROW_SIZE_W
        self.next_page_rect = pygame.Rect(next_page_x_pos, 
                                          page_turn_y_pos - (ARROW_SIZE_H // 2), 
                                          ARROW_SIZE_W, ARROW_SIZE_H)

        # --- Nút Đóng Sổ ---
        CLOSE_BUTTON_SIZE = 25
        # Căn vào góc trên bên phải của sprite đã scale
        self.close_button_rect = pygame.Rect(
            self.BOOK_X + BOOK_TOTAL_WIDTH - CLOSE_BUTTON_SIZE - 15, # 15px padding
            self.BOOK_Y + 15, # 15px padding
            CLOSE_BUTTON_SIZE,
            CLOSE_BUTTON_SIZE
        )

        # === Scale sprite 1 LẦN DUY NHẤT ===
        self.notebook_background_sprite = pygame.transform.scale(
            self.notebook_bg_sprite_original, 
            (BOOK_TOTAL_WIDTH, BOOK_TOTAL_HEIGHT) 
        )

    def open_notebook(self):
        self.is_open = True

    def close_notebook(self):
        self.is_open = False

    def _handle_input(self, event, mouse_pos):
        # ... (Giữ nguyên code) ...
        if event.type == pygame.QUIT:
            self.running = False
        
        if self.is_open: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.close_button_rect.collidepoint(mouse_pos):
                        self.close_notebook()
                        return 
                    
                    if self.prev_page_rect.collidepoint(mouse_pos) and self.current_page > 0:
                        self.current_page = max(0, self.current_page - 1)
                        self.selected_clue_index = -1
                    elif self.next_page_rect.collidepoint(mouse_pos) and self.current_page < self.total_pages - 1:
                        self.current_page = min(self.total_pages - 1, self.current_page + 1)
                        self.selected_clue_index = -1
                    else:
                        for rect_info in self.clue_list_rects:
                            if rect_info and rect_info["rect"].collidepoint(mouse_pos):
                                self.selected_clue_index = rect_info["original_index"]
                                break

    def _update_logic(self):
        # ... (Giữ nguyên code) ...
        if self.is_open: 
            time_in_cycle = pygame.time.get_ticks() % PULSE_CYCLE_MS
            t = time_in_cycle / PULSE_HALF_CYCLE
            if t > 1.0:
                t = 2.0 - t 
            self.current_pulse_color = lerp_color(COLOR_TEXT_BRIGHT, COLOR_TEXT_DIM, t)

    def _draw_close_button(self, mouse_pos):
        # ... (Giữ nguyên code) ...
        button_color = COLOR_CLOSE_BUTTON
        if self.close_button_rect.collidepoint(mouse_pos):
            button_color = COLOR_CLOSE_BUTTON_HOVER
        
        pygame.draw.rect(self.screen, button_color, self.close_button_rect, 0)
        pygame.draw.rect(self.screen, COLOR_BORDER, self.close_button_rect, 1) 

        x_padding = 5
        pygame.draw.line(self.screen, COLOR_BUTTON_TEXT,
                         (self.close_button_rect.left + x_padding, self.close_button_rect.top + x_padding),
                         (self.close_button_rect.right - x_padding, self.close_button_rect.bottom - x_padding), 3)
        pygame.draw.line(self.screen, COLOR_BUTTON_TEXT,
                         (self.close_button_rect.left + x_padding, self.close_button_rect.bottom - x_padding),
                         (self.close_button_rect.right - x_padding, self.close_button_rect.top + x_padding), 3)

    def _draw_open_notebook(self, mouse_pos):
        """Vẽ toàn bộ cuốn sổ khi nó đang mở."""
        
        # 1. Vẽ nền sổ tay (đã được scale)
        self.screen.blit(self.notebook_background_sprite, (self.BOOK_X, self.BOOK_Y))
        
        # 3. Vẽ dòng kẻ (Giữ lại, vì ta dùng sprite KHÔNG CÓ DÒNG KẺ)
        for i in range(CLUES_PER_PAGE):
            # Dòng kẻ trang trái
            y_left = self.CLUE_LIST_AREA_Y + FIRST_LINE_OFFSET_Y + (i * LINE_SPACING)
            pygame.draw.line(self.screen, COLOR_LINE, (self.CLUE_LIST_AREA_X, y_left), (self.CLUE_LIST_AREA_X + self.CLUE_LIST_AREA_WIDTH, y_left), 1)
            # Dòng kẻ trang phải
            y_right = self.INFO_DETAIL_AREA_Y + FIRST_LINE_OFFSET_Y + (i * LINE_SPACING)
            pygame.draw.line(self.screen, COLOR_LINE, (self.INFO_DETAIL_AREA_X, y_right), (self.INFO_DETAIL_AREA_X + self.INFO_DETAIL_AREA_WIDTH, y_right), 1)


        # 4. Vẽ Danh sách Ghi chú (Giữ lại)
        self.clue_list_rects.clear()
        self.clue_list_rects = [None] * len(self.clues)
        
        unlocked_clues = []
        for i, c in enumerate(self.clues):
            if c["unlocked"]:
                unlocked_clues.append({"clue_data": c, "original_index": i})
        
        self.total_pages = max(1, math.ceil(len(unlocked_clues) / CLUES_PER_PAGE))
        
        start_index = self.current_page * CLUES_PER_PAGE
        end_index = start_index + CLUES_PER_PAGE
        clues_to_display = unlocked_clues[start_index:end_index]
        
        # <<< THAY ĐỔI: Trừ đi offset để chữ nằm trên dòng kẻ
        current_y_for_clue_list = (self.CLUE_LIST_AREA_Y + FIRST_LINE_OFFSET_Y) - TEXT_ABOVE_LINE_OFFSET

        font_list = self.fonts['list']

        for i, clue_info in enumerate(clues_to_display):
            # ... (Toàn bộ code vẽ text clue list giữ nguyên) ...
            clue = clue_info["clue_data"]
            original_i = clue_info["original_index"]
            visible_clue_count = start_index + i + 1
            is_selected = (original_i == self.selected_clue_index)
            text_color = self.current_pulse_color if is_selected else COLOR_TEXT_BRIGHT
            
            num_text = f"{visible_clue_count}."
            num_surf = font_list.render(num_text, True, text_color)
            num_rect = num_surf.get_rect(bottomleft=(self.CLUE_LIST_AREA_X, current_y_for_clue_list))
            
            name_text = clue["name"]
            max_name_width = (self.CLUE_LIST_AREA_X + self.CLUE_LIST_AREA_WIDTH) - (num_rect.right + 10)
            name_surf = font_list.render(name_text, True, text_color)
            if name_surf.get_width() > max_name_width:
                truncated_text = name_text
                while font_list.size(truncated_text + "...")[0] > max_name_width and len(truncated_text) > 0:
                    truncated_text = truncated_text[:-1]
                name_text = truncated_text + "..."
                name_surf = font_list.render(name_text, True, text_color)
            name_rect = name_surf.get_rect(bottomleft=(num_rect.right + 10, current_y_for_clue_list))
            
            self.screen.blit(num_surf, num_rect)
            self.screen.blit(name_surf, name_rect)
            
            clickable_rect = pygame.Rect(self.CLUE_LIST_AREA_X,
                                          current_y_for_clue_list - LINE_SPACING + (LINE_SPACING - font_list.get_height()) // 2,
                                          self.CLUE_LIST_AREA_WIDTH,
                                          LINE_SPACING)
            self.clue_list_rects[original_i] = {"rect": clickable_rect, "original_index": original_i}
            
            if is_selected:
                underline_y = current_y_for_clue_list + 1
                start_pos = (num_rect.left, underline_y)
                end_pos = (name_rect.right, underline_y)
                pygame.draw.line(self.screen, COLOR_SELECT_LINE, start_pos, end_pos, 2)
            
            current_y_for_clue_list += LINE_SPACING

        # 5. Vẽ Nút Lật Trang và Số Trang (Giữ lại)
        if self.current_page > 0:
            # ... (Giữ nguyên) ...
            prev_color = COLOR_BUTTON_HOVER if self.prev_page_rect.collidepoint(mouse_pos) else COLOR_BUTTON_TEXT
            pygame.draw.polygon(self.screen, prev_color, [(self.prev_page_rect.right, self.prev_page_rect.top),
                                                         (self.prev_page_rect.right, self.prev_page_rect.bottom),
                                                         (self.prev_page_rect.left, self.prev_page_rect.centery)])
        if self.current_page < self.total_pages - 1:
            # ... (Giữ nguyên) ...
            next_color = COLOR_BUTTON_HOVER if self.next_page_rect.collidepoint(mouse_pos) else COLOR_BUTTON_TEXT
            pygame.draw.polygon(self.screen, next_color, [(self.next_page_rect.left, self.next_page_rect.top),
                                                         (self.next_page_rect.left, self.next_page_rect.bottom),
                                                         (self.next_page_rect.right, self.next_page_rect.centery)])
        
        page_text = f"Page {self.current_page + 1} / {self.total_pages}"
        page_surf = self.fonts['page_count'].render(page_text, True, COLOR_TEXT_DIM)
        # Căn giữa trang phải
        page_rect = page_surf.get_rect(midbottom=(self.INFO_DETAIL_AREA_X + (self.INFO_DETAIL_AREA_WIDTH / 2), self.page_count_y))
        self.screen.blit(page_surf, page_rect)


        # 6. Vẽ Hộp Thông tin (Giữ lại)
        if self.selected_clue_index != -1 and self.clues[self.selected_clue_index]["unlocked"]:
            # ... (Toàn bộ code vẽ text info giữ nguyên) ...
            selected_clue = self.clues[self.selected_clue_index]
            title_text = selected_clue["name"]
            
            font_title_options = self.fonts['title_options']
            font_title_sizes = sorted(font_title_options.keys(), reverse=True)
            selected_title_font = font_title_options[font_title_sizes[-1]]
            title_surf = None
            
            for size in font_title_sizes:
                current_font = font_title_options[size]
                title_surf = current_font.render(title_text, True, COLOR_TEXT_BRIGHT)
                if title_surf.get_width() <= self.INFO_DETAIL_AREA_WIDTH:
                    selected_title_font = current_font
                    break
            
            if title_surf.get_width() > self.INFO_DETAIL_AREA_WIDTH:
                 truncated_text = title_text
                 while selected_title_font.size(truncated_text + "...")[0] > self.INFO_DETAIL_AREA_WIDTH and len(truncated_text) > 0:
                     truncated_text = truncated_text[:-1]
                 title_text = truncated_text + "..."
                 title_surf = selected_title_font.render(title_text, True, COLOR_TEXT_BRIGHT)

            # <<< THAY ĐỔI: Trừ đi offset để tiêu đề nằm trên dòng kẻ
            title_rect = title_surf.get_rect(bottomleft=(self.INFO_DETAIL_AREA_X, self.INFO_DETAIL_AREA_Y + FIRST_LINE_OFFSET_Y - TEXT_ABOVE_LINE_OFFSET))
            self.screen.blit(title_surf, title_rect)
            
            line_y = self.INFO_DETAIL_AREA_Y + FIRST_LINE_OFFSET_Y
            pygame.draw.line(self.screen, COLOR_TEXT_BRIGHT, (self.INFO_DETAIL_AREA_X, line_y), (self.INFO_DETAIL_AREA_X + self.INFO_DETAIL_AREA_WIDTH, line_y), 2)
            
            desc_text = selected_clue["description"]
            max_lines_available = 9
            
            font_desc_options = self.fonts['desc_options']
            font_desc_sizes = sorted(font_desc_options.keys(), reverse=True)
            selected_desc_font = font_desc_options[font_desc_sizes[-1]]
            
            for size in font_desc_sizes:
                current_font = font_desc_options[size]
                if check_text_fit(desc_text, current_font, self.INFO_DETAIL_AREA_WIDTH, max_lines_available, line_height_override=LINE_SPACING):
                    selected_desc_font = current_font
                    break
            
            # <<< THAY ĐỔI: Trừ đi offset để mô tả nằm trên dòng kẻ
            desc_start_y = self.INFO_DETAIL_AREA_Y + FIRST_LINE_OFFSET_Y + (1 * LINE_SPACING) - TEXT_ABOVE_LINE_OFFSET
            desc_end_y = self.INFO_DETAIL_AREA_Y + FIRST_LINE_OFFSET_Y + ((CLUES_PER_PAGE - 1) * LINE_SPACING)
            desc_area_rect = pygame.Rect(self.INFO_DETAIL_AREA_X,
                                         desc_start_y,
                                         self.INFO_DETAIL_AREA_WIDTH,
                                         desc_end_y - desc_start_y + LINE_SPACING)
            draw_text(self.screen, desc_text, selected_desc_font, COLOR_TEXT_BRIGHT, desc_area_rect, line_height_override=LINE_SPACING)

        # Vẽ nút đóng sổ (Giữ lại)
        self._draw_close_button(mouse_pos)

    def draw(self, mouse_pos):
        self.screen.fill(COLOR_DARK_COVER) # Luôn vẽ nền tối
        if self.is_open:
            self._draw_open_notebook(mouse_pos)

    def handle_event(self, event, mouse_pos):
        self._handle_input(event, mouse_pos)

    def update(self):
        self._update_logic()

    def get_state(self):
        return self.is_open