# --- FILE: src/tools/dialogue_data.py ---

# --- DEFINITIONS & COLORS ---
COLOR_PORTRAIT_RED   = (200, 80, 80)    
COLOR_PORTRAIT_BLUE  = (80, 80, 200)    
COLOR_PORTRAIT_GREEN = (80, 200, 80) 
COLOR_PORTRAIT_ANGRY   = (180, 50, 50)   
COLOR_PORTRAIT_ENVY = (100, 200, 100)
COLOR_PORTRAIT_DETECTIVE = (60, 60, 80)      
COLOR_PORTRAIT_WITNESS   = (255, 105, 180)   
COLOR_SYSTEM             = (200, 200, 200)   

all_conversations = {

# ======================================================
    # LUST CASE DIALOGUES (ĐÃ GỘP)
    # ======================================================

    # 1. Khám xét tử thi & Hỏi thăm nhân chứng (GỘP CHUNG)
    "Lust_Body_Exam": [
        # --- PHẦN 1: KHÁM NGHIỆM ---
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "text": "Male victim. Approximately 40 years old. No visible external wounds."
        },
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "text": "There is a spilled wine glass on the carpet. It smells faintly of... bitter almonds."
        },
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "text": "Cyanide? This wasn't an accident. It was murder."
        },
        # Mở khóa manh mối thi thể
        {
            "speaker": "System", 
            "color": COLOR_SYSTEM, 
            "text": "New Clue Added: [Lust Victim]",
            "unlock_clues": ["Lust Victim"], 
            "hide_if_old": True 
        },

        # --- PHẦN 2: CHUYỂN CẢNH SANG HỎI NHÂN CHỨNG ---
        # Thám tử tự động quay sang hỏi người bên cạnh
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "text": "(Turning to the woman nearby) Hello Ma'am. Did you see anyone else here?"
        },
        {
            "speaker": "Witness", 
            "color": COLOR_PORTRAIT_WITNESS, 
            "text": "Oh heavens! Please tell me he is just sleeping!"
        },
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "text": "I'm afraid he's gone. I need to know if you saw anything suspicious."
        },
        {
            "speaker": "Witness", 
            "color": COLOR_PORTRAIT_WITNESS, 
            "text": "I... I saw a woman leaving just minutes ago. She was wearing a stunning red dress."
        },
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "text": "A red dress... interesting."
        },

        # --- PHẦN 3: MỞ KHÓA MANH MỐI NGHI PHẠM ---
        # Mở khóa Clue về nhân chứng/nghi phạm ngay lập tức
        {
            "speaker": "System", 
            "color": COLOR_SYSTEM, 
            "text": "New Clue Added: [Lust Witness]",
            "unlock_clues": ["Lust Witness"], 
            "hide_if_old": True 
        },

        # --- PHẦN 4: LỰA CHỌN TIẾP THEO (TÙY CHỌN) ---
        # Sau khi đã có thông tin cơ bản, cho phép hỏi sâu hơn hoặc kết thúc
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "type": "choice", 
            "text": "I should ask her more details.", 
            "options": [
                {
                    "label": "Did you see any suspicious vehicles?", 
                    "next_id": "Lust_Witness_Vehicle" 
                },
                {
                    "label": "Thank you, that is enough for now.", 
                    "next_id": "Lust_Witness_Bye"
                }
            ]
        }
    ],

    # --- CÁC NHÁNH CON (GIỮ NGUYÊN) ---
    "Lust_Witness_Vehicle": [
        {"speaker": "Witness", "color": COLOR_PORTRAIT_WITNESS, "text": "Actually, yes! I saw a black sedan parked outside for hours."},
        {"speaker": "Detective", "color": COLOR_PORTRAIT_DETECTIVE, "text": "Interesting. That matches the description of a known criminal's car."},
        
        {
            "speaker": "System", 
            "color": COLOR_SYSTEM, 
            "text": "New Clue Added: [Witness Sighting]",
            "unlock_clues": ["Witness Sighting"], 
            "hide_if_old": True                   
        }
    ],

    "Lust_Witness_Bye": [
        {"speaker": "Detective", "color": COLOR_PORTRAIT_DETECTIVE, "text": "Stay safe, Ma'am."}
    ],

    # --- NHÁNH DỰ PHÒNG ---
    # Nếu người chơi lỡ bấm thoát và muốn hỏi lại nhân chứng trực tiếp (bấm vào NPC)
    # thì vẫn nên giữ lại đoạn này, nhưng nội dung ngắn gọn hơn.
    "Lust_Witness_Talk": [
        {
            "speaker": "Witness", 
            "color": COLOR_PORTRAIT_WITNESS, 
            "text": "That poor man... The woman in the red dress..."
        },
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "type": "choice", 
            "text": "Ask details:", 
            "options": [
                {
                    "label": "Did you see any suspicious vehicles?", 
                    "next_id": "Lust_Witness_Vehicle"
                },
                {
                    "label": "Goodbye.", 
                    "next_id": "Lust_Witness_Bye"
                }
            ]
        }
    ],
    # ======================================================
    # WRATH CASE DIALOGUES 
    # ======================================================

    # Hội thoại với nạn nhân (hoặc môn sinh đang tức giận)
    "Wrath_Angry_Victim": [
        {
            "speaker": "Angry Student", 
            "color": COLOR_PORTRAIT_ANGRY, 
            "text": "Get lost! Can't you see we are mourning?!"
        },
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "text": "I am here to help. I need to know who attacked your master."
        },
        {
            "speaker": "Angry Student", 
            "color": COLOR_PORTRAIT_ANGRY, 
            "text": "It was HIM! That coward from the Cobra Dojo! He couldn't win fairly, so he used dirty tricks!"
        },
        
        # --- LỰA CHỌN ---
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "type": "choice", 
            "text": "How should I respond?", 
            "options": [
                {
                    "label": "Calm down, anger won't help.", 
                    "next_id": "Wrath_Calm_Down"
                },
                {
                    "label": "Tell me more about this 'Cobra Dojo'.", 
                    "next_id": "Wrath_Rivalry_Info"
                    # Không để unlock ở đây để tránh lỗi logic cũ
                },
                {
                    "label": "I'll leave you alone.", 
                    "next_id": "Wrath_Leave"
                }
            ]
        }
    ],

    # --- NHÁNH CON WRATH ---
    "Wrath_Calm_Down": [
        {"speaker": "Angry Student", "color": COLOR_PORTRAIT_ANGRY, "text": "Don't tell me to calm down! My master is dead!"}
    ],

    "Wrath_Rivalry_Info": [
        {"speaker": "Detective", "color": COLOR_PORTRAIT_DETECTIVE, "text": "Was there a history of violence between the dojos?"},
        {"speaker": "Angry Student", "color": COLOR_PORTRAIT_ANGRY, "text": "Yes! They threatened to burn us down last week. This must be their doing!"},
        
        # --- MỞ KHÓA MANH MỐI & THÔNG BÁO ---
        {
            "speaker": "System", 
            "color": COLOR_SYSTEM, 
            "text": "New Clue Added: [Dojo Rivalry]",
            "unlock_clues": ["Dojo Rivalry"], 
            "hide_if_old": True 
        }
    ],

    "Wrath_Leave": [
        {"speaker": "Detective", "color": COLOR_PORTRAIT_DETECTIVE, "text": "I will find justice for your master."}
    ],
    # ======================================================
    # ENVY CASE DIALOGUES 
    # ======================================================
    "Envy_Suspect_Talk": [
        {
            "speaker": "Jealous Actor", 
            "color": COLOR_PORTRAIT_ENVY, 
            "text": "What do you want? I'm busy rehearsing lines that *should* have been mine."
        },
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "text": "I'm investigating the death on stage. You seem upset."
        },
        {
            "speaker": "Jealous Actor", 
            "color": COLOR_PORTRAIT_ENVY, 
            "text": "Upset? No. I'm furious. She didn't have the talent! She only got the lead role because of her connections!"
        },
        {
            "speaker": "Detective", 
            "color": COLOR_PORTRAIT_DETECTIVE, 
            "type": "choice", 
            "text": "Dig deeper:", 
            "options": [
                {
                    "label": "Did you hate her enough to kill her?", 
                    "next_id": "Envy_Kill_Question"
                },
                {
                    "label": "Tell me about the role.", 
                    "next_id": "Envy_Role_Info"
                },
                {
                    "label": "Goodbye.", 
                    "next_id": "Envy_Leave"
                }
            ]
        }
    ],

    # --- NHÁNH CON ENVY ---
    "Envy_Kill_Question": [
        {"speaker": "Jealous Actor", "color": COLOR_PORTRAIT_ENVY, "text": "I wanted her gone from the play, not from life! I'm an artist, not a murderer!"}
    ],

    "Envy_Role_Info": [
        {"speaker": "Jealous Actor", "color": COLOR_PORTRAIT_ENVY, "text": "It was the role of a lifetime. The 'Phantom Queen'. I prepared for months, but she stole it!"},
        
        # Mở khóa manh mối động cơ
        {
            "speaker": "System", 
            "color": COLOR_SYSTEM, 
            "text": "New Clue Added: [Stolen Role]",
            "unlock_clues": ["Stolen Role"], 
            "hide_if_old": True 
        }
    ],

    "Envy_Leave": [
        {"speaker": "Detective", "color": COLOR_PORTRAIT_DETECTIVE, "text": "Don't leave town."}
    ],
    
}