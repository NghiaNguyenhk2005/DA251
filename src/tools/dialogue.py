# --- FILE: src/tools/dialogue.py ---
import pygame
import os 
import sys

# --- IMPORT FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.tools.dialogue_data import all_conversations
from src.tools.game_state import game_state 
from src.tools.Notebook_clues import clues

# --- CONSTANTS ---
COLOR_BG_DARK = (28, 28, 36)         
COLOR_BORDER_GOLD = (196, 145, 60)   
COLOR_BORDER_SHADOW = (105, 75, 30)  
COLOR_TEXT_WHITE = (235, 235, 235)   
COLOR_TEXT_GREY = (150, 150, 160)    
COLOR_NAME_TAG_BG = (45, 40, 50)     
COLOR_OPTION_BG = (40, 40, 50)       
COLOR_OPTION_HOVER = (70, 70, 90)    
COLOR_OPTION_BORDER = (100, 100, 100)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# --- PATH CONFIG ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
ASSETS_DIR = os.path.join(SRC_DIR, "assets")

class NPC:
    def __init__(self, x, y, width, height, color, dialogue_id):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.dialogue_id = dialogue_id 
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2) 

class DialogueBox:
    def __init__(self, screen):
        self.screen = screen
        
        # --- LOAD FONT ---
        font_path = os.path.join(ASSETS_DIR, "fonts", "Harmonic.ttf")
        try:
            self.font = pygame.font.Font(font_path, 24)
            self.name_font = pygame.font.Font(font_path, 26)
        except FileNotFoundError:
            self.font = pygame.font.SysFont("Consolas", 20)
            self.name_font = pygame.font.SysFont("Consolas", 24, bold=True)
        
        # --- UI CONFIG ---
        self.box_height = 160 
        self.box_width = SCREEN_WIDTH - 100
        self.box_x = 50
        
        self.avatar_size = (self.box_height, self.box_height) 
        self.avatar_cache = {}        

        # --- LOAD AVATAR ---
        default_avatar_path = os.path.join(ASSETS_DIR, "character_avatars", "default_avatar.png")
        try:
            raw_img = pygame.image.load(default_avatar_path).convert_alpha()
            self.default_avatar = pygame.transform.scale(raw_img, self.avatar_size)
        except (FileNotFoundError, pygame.error):
            self.default_avatar = pygame.Surface(self.avatar_size)
            self.default_avatar.fill((50, 50, 50)) 

        # --- ANIMATION ---
        self.pos_y_normal = SCREEN_HEIGHT - self.box_height - 30
        self.target_y = self.pos_y_normal  
        self.current_y = self.pos_y_normal 
        self.anim_speed = 0.15             

        # --- STATE ---
        self.dialogue_queue = [] 
        self.current_dialogue = None
        self.is_active = False 
        
        # Typing
        self.display_text_lines = []
        self.target_text_lines = []
        self.char_timer = 0
        self.char_interval = 25 
        self.line_index = 0      
        self.char_index = 0      
        self.is_typing = False

        # Choices
        self.is_choice_mode = False
        self.current_options = []
        self.selected_option_index = 0
        self.option_rects = [] 
        
        self.OPTION_HEIGHT = 45
        self.OPTION_GAP = 5

    def start_conversation(self, conversation_id):
        if conversation_id in all_conversations:
            data = all_conversations[conversation_id]
            self.dialogue_queue = list(data)
            
            if not self.is_active:
                self.current_y = self.pos_y_normal
                self.target_y = self.pos_y_normal
            
            self.is_active = True
            self.next_dialogue()
        else:
            print(f"Error: Dialogue ID '{conversation_id}' not found.")
    
    # --- LOGIC MỞ KHÓA (CẬP NHẬT: TRẢ VỀ TRUE/FALSE) ---
    def unlock_clues_in_notebook(self, clue_names_list):
        """Trả về True nếu có ít nhất 1 manh mối MỚI được mở."""
        any_new = False # Biến cờ theo dõi
        
        print(f"🔍 Checking clues: {clue_names_list}")
        for name_to_unlock in clue_names_list:
            found = False
            for clue in clues:
                if clue["name"] == name_to_unlock:
                    if not clue["unlocked"]:
                        clue["unlocked"] = True
                        any_new = True # Đã tìm thấy cái mới!
                        print(f"🔓 UNLOCKED NEW CLUE: {name_to_unlock}")
                    else:
                        print(f"ℹ️ Clue '{name_to_unlock}' already known.")
                    found = True
                    break
            if not found:
                print(f"⚠️ Warning: Clue '{name_to_unlock}' not found in Notebook_clues.py!")
        
        return any_new

    def next_dialogue(self):
        if len(self.dialogue_queue) > 0:
            self.current_dialogue = self.dialogue_queue.pop(0)
            
            # --- 1. XỬ LÝ MỞ KHÓA ---
            is_new_clue = False
            if "unlock_clues" in self.current_dialogue:
                is_new_clue = self.unlock_clues_in_notebook(self.current_dialogue["unlock_clues"])

            # --- 2. XỬ LÝ BỎ QUA (SKIP) NẾU CŨ ---
            # Nếu dòng thoại này có cờ 'hide_if_old' = True VÀ không có manh mối mới -> Bỏ qua
            if self.current_dialogue.get("hide_if_old", False) and not is_new_clue:
                print("⏩ Skipping notification (Clue already known).")
                self.next_dialogue() # Gọi đệ quy để sang câu tiếp theo ngay lập tức
                return

            # --- 3. HIỂN THỊ ---
            raw_text = self.current_dialogue["text"]
            text_padding_left = 30
            self.text_width = self.box_width - self.avatar_size[0] - text_padding_left - 20
            
            self.target_text_lines = self.wrap_text(raw_text)
            self.display_text_lines = [""]
            self.line_index = 0
            self.char_index = 0
            self.is_typing = True
            self.char_timer = pygame.time.get_ticks()

            if self.current_dialogue.get("type") == "choice":
                self.is_choice_mode = True
                self.current_options = self.current_dialogue["options"]
                self.selected_option_index = 0
                
                num_options = len(self.current_options)
                total_options_height = num_options * (self.OPTION_HEIGHT + self.OPTION_GAP) + 20 
                self.target_y = self.pos_y_normal - total_options_height
            else:
                self.is_choice_mode = False
                self.target_y = self.pos_y_normal 
        else:
            self.is_active = False 
            self.current_dialogue = None
            self.is_choice_mode = False

    def wrap_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < self.text_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines

    def update(self):
        if not self.is_active: return
        
        diff = self.target_y - self.current_y
        if abs(diff) > 0.5:
            self.current_y += diff * self.anim_speed
        else:
            self.current_y = self.target_y

        if self.is_typing:
            current_time = pygame.time.get_ticks()
            if current_time - self.char_timer > self.char_interval:
                self.char_timer = current_time
                if self.line_index < len(self.target_text_lines):
                    target_line = self.target_text_lines[self.line_index]
                    if self.char_index < len(target_line):
                        while len(self.display_text_lines) <= self.line_index: self.display_text_lines.append("")
                        self.display_text_lines[self.line_index] += target_line[self.char_index]
                        self.char_index += 1
                    else:
                        self.line_index += 1
                        self.char_index = 0
                        if self.line_index < len(self.target_text_lines): self.display_text_lines.append("")
                else:
                    self.is_typing = False

    def get_avatar_for_speaker(self, speaker_name):
        if speaker_name in self.avatar_cache:
            return self.avatar_cache[speaker_name]
        
        clean_name = speaker_name.strip().lower().replace(" ", "_")
        filename = f"{clean_name}.png"
        full_path = os.path.join(ASSETS_DIR, "character_avatars", filename)
        
        try:
            image = pygame.image.load(full_path).convert_alpha()
            image = pygame.transform.scale(image, self.avatar_size)
            self.avatar_cache[speaker_name] = image
            return image
        except (FileNotFoundError, pygame.error):
            self.avatar_cache[speaker_name] = self.default_avatar
            return self.default_avatar

    # --- INPUT HANDLERS ---
    def handle_choice_key_input(self, key):
        if not self.is_choice_mode or self.is_typing: return
        if key == pygame.K_UP or key == pygame.K_w:
            self.selected_option_index = max(0, self.selected_option_index - 1)
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.selected_option_index = min(len(self.current_options) - 1, self.selected_option_index + 1)
        elif key == pygame.K_SPACE or key == pygame.K_RETURN:
            self._confirm_choice(self.selected_option_index)

    def handle_mouse_move(self, mouse_pos):
        if not self.is_choice_mode or self.is_typing: return
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_option_index = i
                return

    def handle_mouse_click_choice(self, mouse_pos):
        if not self.is_choice_mode or self.is_typing: return False
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self._confirm_choice(i)
                return True
        return False

    def _confirm_choice(self, index):
        chosen_option = self.current_options[index]
        
        if "money_change" in chosen_option:
            amount = chosen_option["money_change"]
            game_state["money"] += amount
            print(f"Money updated: {game_state['money']}")
            
        # Lưu ý: Ta đã chuyển logic unlock clues vào bên trong nhánh hội thoại (dialogue_data)
        # nên ở đây có thể giữ hoặc bỏ cũng được, nhưng tốt nhất cứ để hỗ trợ cả 2 cách.
        if "unlock_clues" in chosen_option:
            self.unlock_clues_in_notebook(chosen_option["unlock_clues"])
        
        next_id = chosen_option.get("next_id")
        if next_id:
            self.start_conversation(next_id)
        else:
            self.next_dialogue()

    def handle_input(self):
        if not self.is_active: return
        if self.is_choice_mode:
            if self.is_typing:
                self.display_text_lines = self.target_text_lines[:]
                self.is_typing = False
            return 
        if self.is_typing:
            self.display_text_lines = self.target_text_lines[:]
            self.is_typing = False
        else:
            self.next_dialogue()

    # --- DRAWING ---
    def draw_pixel_box(self, rect, bg_color, border_color):
        if bg_color is not None:
            pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 4) 
        pygame.draw.rect(self.screen, border_color, rect.inflate(-4, -4), 2) 
        pygame.draw.rect(self.screen, (0, 0, 0), rect.inflate(-8, -8), 2)

    def draw(self):
        if not self.is_active or not self.current_dialogue: return
        y_pos = int(self.current_y)
        main_rect = pygame.Rect(self.box_x, y_pos, self.box_width, self.box_height)
        self.draw_pixel_box(main_rect, COLOR_BG_DARK, COLOR_BORDER_GOLD)
        
        portrait_x = self.box_x
        portrait_y = y_pos
        portrait_rect = pygame.Rect(portrait_x, portrait_y, self.avatar_size[0], self.avatar_size[1])
        inner_portrait_rect = portrait_rect.inflate(-8, -8)
        pygame.draw.rect(self.screen, self.current_dialogue["color"], inner_portrait_rect)
        
        speaker_name = self.current_dialogue["speaker"]
        avatar_surf = self.get_avatar_for_speaker(speaker_name)
        self.screen.blit(avatar_surf, (portrait_x, portrait_y)) 
        self.draw_pixel_box(portrait_rect, None, COLOR_BORDER_GOLD) 

        name_text = self.current_dialogue["speaker"]
        name_surf = self.name_font.render(name_text, True, COLOR_BORDER_GOLD)
        name_rect_w = name_surf.get_width() + 30
        name_rect_h = 36
        name_rect_x = portrait_rect.centerx - (name_rect_w // 2)
        name_rect_y = y_pos - 20 
        name_rect = pygame.Rect(name_rect_x, name_rect_y, name_rect_w, name_rect_h)
        self.draw_pixel_box(name_rect, COLOR_NAME_TAG_BG, COLOR_BORDER_GOLD)
        self.screen.blit(name_surf, (name_rect.centerx - name_surf.get_width()//2, name_rect.centery - name_surf.get_height()//2))

        text_start_x = portrait_x + self.avatar_size[0] + 30
        text_start_y = y_pos + 30
        line_height = self.font.get_linesize()
        for i, line in enumerate(self.display_text_lines):
            text_surf = self.font.render(line, False, COLOR_TEXT_WHITE)
            self.screen.blit(text_surf, (text_start_x, text_start_y + i * line_height))

        if self.is_choice_mode and not self.is_typing:
            self.option_rects.clear() 
            start_y_options = y_pos + self.box_height + 10
            option_w = self.box_width
            option_h = self.OPTION_HEIGHT
            for index, option in enumerate(self.current_options):
                is_selected = (index == self.selected_option_index)
                bg_col = COLOR_OPTION_HOVER if is_selected else COLOR_OPTION_BG
                border_col = COLOR_BORDER_GOLD if is_selected else COLOR_OPTION_BORDER
                text_col = COLOR_TEXT_WHITE if is_selected else COLOR_TEXT_GREY
                opt_rect = pygame.Rect(self.box_x, start_y_options + index * (option_h + self.OPTION_GAP), option_w, option_h)
                self.option_rects.append(opt_rect)
                self.draw_pixel_box(opt_rect, bg_col, border_col)
                if is_selected:
                    pygame.draw.polygon(self.screen, COLOR_BORDER_GOLD, [
                        (opt_rect.x + 15, opt_rect.centery - 6),
                        (opt_rect.x + 15, opt_rect.centery + 6),
                        (opt_rect.x + 25, opt_rect.centery)
                    ])
                label = option["label"]
                opt_surf = self.font.render(label, False, text_col)
                opt_text_rect = opt_surf.get_rect(center=opt_rect.center)
                self.screen.blit(opt_surf, opt_text_rect)

        elif not self.is_typing and not self.is_choice_mode:
            t = pygame.time.get_ticks() % 1000
            offset = 0 if t < 500 else 5
            arrow_x = self.box_x + self.box_width - 40
            arrow_y = y_pos + self.box_height - 30 + offset
            pygame.draw.polygon(self.screen, COLOR_BORDER_GOLD, [
                (arrow_x, arrow_y),
                (arrow_x + 20, arrow_y),
                (arrow_x + 10, arrow_y + 10)
            ])