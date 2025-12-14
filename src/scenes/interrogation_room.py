import pygame
from typing import Optional, List, Dict, Callable
from .i_scene import IScene


class InterrogationRoomScene(IScene):
    def __init__(self, screen_width: int = 800, screen_height: int = 600, on_interrogation_complete: Optional[Callable] = None, background_path: Optional[str] = None) -> None:
        """
        Interrogation room scene with question/answer system
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
            on_interrogation_complete: Callback when all questions answered correctly
            background_path: Custom background path (from suspect selection)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.on_interrogation_complete = on_interrogation_complete
        
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
        
        # Interrogation questions (5 questions)
        self.questions = [
            {
                "question": "Where were you at 8 PM last night?",
                "choices": [
                    "I was at home alone",
                    "I was at the victim's office", 
                    "I was at a restaurant with friends"
                ],
                "correct": 0  # Index of correct answer
            },
            {
                "question": "What is your relationship with the victim?",
                "choices": [
                    "We were business partners",
                    "I barely knew them",
                    "We were close friends"
                ],
                "correct": 0
            },
            {
                "question": "Why did you have the victim's keys?",
                "choices": [
                    "I found them on the street",
                    "The victim gave them to me",
                    "I took them from the office"
                ],
                "correct": 0
            },
            {
                "question": "What was the argument about yesterday?",
                "choices": [
                    "There was no argument",
                    "Money and business disputes",
                    "Personal matters"
                ],
                "correct": 0
            },
            {
                "question": "Can you explain the evidence found at the scene?",
                "choices": [
                    "I was framed by someone",
                    "I accidentally left them there",
                    "Those items were planted"
                ],
                "correct": 0
            }
        ]
        
        # State management
        self.current_question = 0
        self.selected_choice = 0
        self.correct_answers = 0
        self.answered_questions = []
        self.show_result = False
        self.result_message = ""
        self.result_timer = 0
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events for this scene"""
        if event.type == pygame.KEYDOWN:
            if self.show_result:
                # After showing result, go to next question or finish
                if event.key == pygame.K_RETURN:
                    self.show_result = False
                    self.current_question += 1
                    
                    # Check if all questions answered
                    if self.current_question >= len(self.questions):
                        if self.correct_answers == len(self.questions):
                            # All correct! Go to accusation system
                            print(f"✅ All {len(self.questions)} questions correct! Opening accusation system...")
                            if self.on_interrogation_complete:
                                self.on_interrogation_complete()
                        else:
                            # Failed - reset interrogation
                            print(f"❌ Only {self.correct_answers}/{len(self.questions)} correct. Restarting...")
                            self.reset_interrogation()
                return
            
            if event.key == pygame.K_UP:
                self.selected_choice = (self.selected_choice - 1) % len(self.questions[self.current_question]["choices"])
            elif event.key == pygame.K_DOWN:
                self.selected_choice = (self.selected_choice + 1) % len(self.questions[self.current_question]["choices"])
            elif event.key == pygame.K_RETURN:
                # Check answer
                correct_answer = self.questions[self.current_question]["correct"]
                if self.selected_choice == correct_answer:
                    self.correct_answers += 1
                    self.result_message = "CORRECT!"
                else:
                    self.result_message = "WRONG!"
                
                self.answered_questions.append({
                    "question_idx": self.current_question,
                    "selected": self.selected_choice,
                    "correct": self.selected_choice == correct_answer
                })
                
                self.show_result = True
                self.result_timer = 60  # Show for 1 second
                self.selected_choice = 0  # Reset selection for next question
    
    def reset_interrogation(self):
        """Reset interrogation to start over"""
        self.current_question = 0
        self.selected_choice = 0
        self.correct_answers = 0
        self.answered_questions = []
        self.show_result = False
    
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
            # Show result message
            color = (0, 255, 0) if self.result_message == "CORRECT!" else (255, 0, 0)
            result_text = self.result_font.render(self.result_message, True, color)
            result_rect = result_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(result_text, result_rect)
            
            # Show score
            score_text = self.choice_font.render(
                f"Score: {self.correct_answers}/{self.current_question + 1}", 
                True, (255, 255, 255)
            )
            score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))
            screen.blit(score_text, score_rect)
            
            # Instruction
            continue_text = self.choice_font.render("Press ENTER to continue", True, (200, 200, 200))
            continue_rect = continue_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))
            screen.blit(continue_text, continue_rect)
        else:
            # Draw question number and progress
            progress_text = self.choice_font.render(
                f"Question {self.current_question + 1}/{len(self.questions)}", 
                True, (255, 255, 255)
            )
            screen.blit(progress_text, (50, 50))
            
            # Draw current question
            question = self.questions[self.current_question]
            
            # Word wrap question text
            question_lines = self.wrap_text(question["question"], self.question_font, self.screen_width - 100)
            y_offset = 120
            for line in question_lines:
                question_surface = self.question_font.render(line, True, (255, 255, 255))
                screen.blit(question_surface, (50, y_offset))
                y_offset += 35
            
            # Draw choices
            y_offset += 40
            for i, choice in enumerate(question["choices"]):
                # Highlight selected choice
                if i == self.selected_choice:
                    color = (255, 255, 0)
                    prefix = "> "
                else:
                    color = (200, 200, 200)
                    prefix = "  "
                
                # Wrap choice text
                choice_lines = self.wrap_text(f"{prefix}{i + 1}. {choice}", self.choice_font, self.screen_width - 120)
                for line in choice_lines:
                    choice_surface = self.choice_font.render(line, True, color)
                    screen.blit(choice_surface, (70, y_offset))
                    y_offset += 30
                y_offset += 10  # Extra spacing between choices
            
            # Instructions
            instruction_text = self.choice_font.render("UP/DOWN to select, ENTER to confirm", True, (150, 150, 150))
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
            screen.blit(instruction_text, instruction_rect)
    
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
