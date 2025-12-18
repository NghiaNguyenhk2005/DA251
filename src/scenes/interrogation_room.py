import pygame
from typing import Optional, List, Dict, Callable
from .i_scene import IScene


class InterrogationRoomScene(IScene):
    def __init__(self, screen_width: int = 800, screen_height: int = 600, on_interrogation_complete: Optional[Callable] = None, background_path: Optional[str] = None, suspect_index: int = 0, on_back: Optional[Callable] = None) -> None:
        """
        Interrogation room scene with question/answer system
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
            on_interrogation_complete: Callback when all questions answered correctly
            background_path: Custom background path (from suspect selection)
            suspect_index: Which suspect is being interrogated (0=John Doe, 1=Jane Smith, 2=Victor)
            on_back: Callback when player wants to go back to office
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.on_interrogation_complete = on_interrogation_complete
        self.on_back = on_back
        self.suspect_index = suspect_index
        
        # Suspect names for display
        self.suspect_names = ["John Doe", "Jane Smith", "Victor Reznov"]
        self.current_suspect_name = self.suspect_names[suspect_index]
        
        # Load and scale background
        bg_path = background_path or "assets/images/scenes/interrogation-bg.png"
        try:
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(
                self.background, 
                (screen_width, screen_height)
            )
            print(f"✅ Loaded interrogation background: {bg_path}")
        except Exception as e:
            print(f"⚠️ Could not load {bg_path}: {e}")
            # Fallback: create a dark background
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill((30, 30, 40))
        
        # Font setup
        try:
            self.question_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 20)
            self.choice_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 16)
            self.result_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 24)
        except:
            self.question_font = pygame.font.Font(None, 28)
            self.choice_font = pygame.font.Font(None, 24)
            self.result_font = pygame.font.Font(None, 32)
        
        # Interrogation questions (10 questions)
        # Each question has 3 answers (one for each suspect)
        # suspicious: True = doesn't match evidence (inconsistent)
        self.questions = [
            {
                "question": "Where were you at the time of the incident?",
                "answers": [
                    {"text": "I was at home with my family.", "suspicious": False},  # John Doe
                    {"text": "I was outside alone, no one witnessed.", "suspicious": True},  # Jane Smith
                    {"text": "I was near the scene but not involved.", "suspicious": False}  # Victor
                ]
            },
            {
                "question": "Did you know the victim?",
                "answers": [
                    {"text": "Yes, we were friends/colleagues.", "suspicious": True},  # John Doe
                    {"text": "No, I've never met them.", "suspicious": False},  # Jane Smith
                    {"text": "I only knew them briefly, not close.", "suspicious": False}  # Victor
                ]
            },
            {
                "question": "Why did you appear near the crime scene?",
                "answers": [
                    {"text": "I just happened to pass by.", "suspicious": True},  # John Doe
                    {"text": "I went there to meet someone else.", "suspicious": False},  # Jane Smith
                    {"text": "I don't remember clearly, might have taken wrong turn.", "suspicious": False}  # Victor
                ]
            },
            {
                "question": "What transportation did you use that day?",
                "answers": [
                    {"text": "I used my motorcycle.", "suspicious": False},  # John Doe
                    {"text": "I walked, didn't use any vehicle.", "suspicious": True},  # Jane Smith
                    {"text": "I borrowed a friend's vehicle.", "suspicious": False}  # Victor
                ]
            },
            {
                "question": "Can you explain the evidence/items found related to you?",
                "answers": [
                    {"text": "Those were mine but I lost them before.", "suspicious": True},  # John Doe
                    {"text": "I don't know why they appeared there.", "suspicious": False},  # Jane Smith
                    {"text": "Someone might have taken my items and left them.", "suspicious": False}  # Victor
                ]
            },
            {
                "question": "Do you have anyone to verify your statement?",
                "answers": [
                    {"text": "Yes, family/friends can confirm.", "suspicious": False},  # John Doe
                    {"text": "No, I was alone.", "suspicious": False},  # Jane Smith
                    {"text": "I think someone saw me but we're not acquainted.", "suspicious": True}  # Victor
                ]
            },
            {
                "question": "What items were you carrying when passing by?",
                "answers": [
                    {"text": "I only had my phone and wallet.", "suspicious": True},  # John Doe
                    {"text": "I had a bag with me, but it's unrelated.", "suspicious": False},  # Jane Smith
                    {"text": "I don't remember clearly, maybe nothing.", "suspicious": False}  # Victor
                ]
            },
            {
                "question": "Did you have any conflict with the victim before?",
                "answers": [
                    {"text": "Yes, we argued but resolved it.", "suspicious": False},  # John Doe
                    {"text": "No, I never had any issues.", "suspicious": False},  # Jane Smith
                    {"text": "No, I didn't even know them.", "suspicious": True}  # Victor
                ]
            },
            {
                "question": "Do you know anyone else who might be involved?",
                "answers": [
                    {"text": "I think there's someone more suspicious.", "suspicious": False},  # John Doe
                    {"text": "I don't know anyone.", "suspicious": False},  # Jane Smith
                    {"text": "There are people who often contacted the victim.", "suspicious": True}  # Victor
                ]
            },
            {
                "question": "Are you willing to cooperate with the investigation?",
                "answers": [
                    {"text": "Yes, I'll provide all necessary information.", "suspicious": True},  # John Doe
                    {"text": "I'll only answer within my lawyer's permission.", "suspicious": False},  # Jane Smith
                    {"text": "I don't want to say anything more.", "suspicious": False}  # Victor
                ]
            }
        ]
        
        # State management
        self.current_question = 0
        self.correct_answers = 0
        self.answered_questions = []
        self.show_result = False
        self.result_message = ""
        self.result_timer = 0
        self.waiting_for_judgment = False  # True when showing answer, waiting for player judgment
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events for this scene"""
        if event.type == pygame.KEYDOWN:
            # ESC to go back to office
            if event.key == pygame.K_ESCAPE:
                print("🔙 Going back to office...")
                if self.on_back:
                    self.on_back()
                return
            
            if self.show_result:
                # Interrogation complete, proceed to accusation
                if event.key == pygame.K_RETURN:
                    print(f"✅ Interrogation complete! Proceeding to accusation...")
                    if self.on_interrogation_complete:
                        self.on_interrogation_complete()
                return
            
            if self.waiting_for_judgment:
                # Player is judging the suspect's answer
                # Y = mark as INCONSISTENT/Suspicious
                # N = mark as CONSISTENT/Normal
                player_judges_suspicious = False
                
                if event.key == pygame.K_y:
                    player_judges_suspicious = True
                elif event.key == pygame.K_n:
                    player_judges_suspicious = False
                else:
                    return  # Invalid key, wait for Y or N
                
                # Record the answer
                self.answered_questions.append({
                    "question_idx": self.current_question,
                    "player_judgment": player_judges_suspicious
                })
                
                # Move to next question immediately (no result display)
                self.waiting_for_judgment = False
                self.current_question += 1
                
                # Check if all questions answered
                if self.current_question >= len(self.questions):
                    # All questions answered - show finish screen
                    self.show_result = True
            else:
                # Show suspect's answer when player presses ENTER
                if event.key == pygame.K_RETURN:
                    self.waiting_for_judgment = True
    
    def reset_interrogation(self):
        """Reset interrogation to start over"""
        self.current_question = 0
        self.correct_answers = 0
        self.answered_questions = []
        self.show_result = False
        self.waiting_for_judgment = False
    
    def update(self) -> None:
        """Update scene state"""
        if self.show_result and self.result_timer > 0:
            self.result_timer -= 1
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the scene"""
        screen.blit(self.background, (0, 0))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        if self.show_result:
            # Interrogation complete - show accusation button
            complete_text = self.result_font.render("INTERROGATION COMPLETE", True, (255, 255, 100))
            complete_rect = complete_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
            screen.blit(complete_text, complete_rect)
            
            # Show number of questions answered
            answered_text = self.choice_font.render(
                f"Answered {len(self.answered_questions)} questions", 
                True, (200, 200, 200)
            )
            answered_rect = answered_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(answered_text, answered_rect)
            
            # Instruction to proceed to accusation
            instruction_text = self.choice_font.render("Press ENTER to proceed to ACCUSATION", True, (100, 255, 100))
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
            screen.blit(instruction_text, instruction_rect)
            
            # ESC to go back
            back_text = self.choice_font.render("Press ESC to return to Office", True, (255, 100, 100))
            back_rect = back_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 120))
            screen.blit(back_text, back_rect)
        else:
            # Draw question number and progress
            progress_text = self.choice_font.render(
                f"Question {self.current_question + 1}/{len(self.questions)} - Interrogating: {self.current_suspect_name}", 
                True, (255, 255, 255)
            )
            screen.blit(progress_text, (50, 50))
            
            # Draw current question
            question = self.questions[self.current_question]
            
            # Word wrap question text
            question_lines = self.wrap_text(question["question"], self.question_font, self.screen_width - 100)
            y_offset = 120
            
            # Draw "Detective:" label
            detective_label = self.question_font.render("Detective:", True, (100, 200, 255))
            screen.blit(detective_label, (50, y_offset))
            y_offset += 40
            
            for line in question_lines:
                question_surface = self.question_font.render(line, True, (255, 255, 255))
                screen.blit(question_surface, (70, y_offset))
                y_offset += 35
            
            if self.waiting_for_judgment:
                # Show suspect's answer
                y_offset += 40
                suspect_label = self.question_font.render(f"{self.current_suspect_name}:", True, (255, 200, 100))
                screen.blit(suspect_label, (50, y_offset))
                y_offset += 40
                
                # Get and display suspect's answer
                suspect_answer = question["answers"][self.suspect_index]
                answer_lines = self.wrap_text(suspect_answer["text"], self.choice_font, self.screen_width - 120)
                for line in answer_lines:
                    answer_surface = self.choice_font.render(line, True, (220, 220, 220))
                    screen.blit(answer_surface, (70, y_offset))
                    y_offset += 30
                
                # Instructions for judgment
                y_offset += 40
                instruction_text = self.choice_font.render("Judge the statement:", True, (255, 255, 100))
                screen.blit(instruction_text, (70, y_offset))
                y_offset += 35
                
                y_option = self.choice_font.render("Y - Mark as INCONSISTENT (Suspicious)", True, (255, 150, 150))
                screen.blit(y_option, (70, y_offset))
                y_offset += 30
                
                n_option = self.choice_font.render("N - Mark as CONSISTENT (Normal)", True, (150, 255, 150))
                screen.blit(n_option, (70, y_offset))
            else:
                # Show instruction to ask question
                y_offset += 60
                instruction_text = self.choice_font.render("Press ENTER to ask the question", True, (150, 150, 150))
                instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, y_offset))
                screen.blit(instruction_text, instruction_rect)
            
            # Draw BACK button instruction at bottom
            back_text = self.choice_font.render("Press ESC to return to Office", True, (200, 100, 100))
            back_rect = back_text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
            screen.blit(back_text, back_rect)
    
    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]
