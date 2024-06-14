import customtkinter as ctk

ctk.set_appearance_mode("dark")

WINDDOW_WIDTH = 650
WINDDOW_HEIGHT = 600
X_PADDING = 30
Y_PADDING = 10
CORNER_RADIUS = 15

class ChatView(ctk.CTk):
    def __init__(self, controller):
        super().__init__() 
        FONT = ctk.CTkFont(family="Arial", size=14)

        self.title("MyChat")
        self.geometry(f"{WINDDOW_WIDTH}x{WINDDOW_HEIGHT}")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.chat_box = ctk.CTkTextbox(self, corner_radius=CORNER_RADIUS, font=FONT)
        self.chat_box.grid(column=0, row=0, padx=X_PADDING, pady=Y_PADDING, sticky="news", columnspan=2)


        self.user_part = ctk.CTkFrame(self, corner_radius=CORNER_RADIUS)
        self.user_part.grid(column=0, row=1, padx=X_PADDING, pady=Y_PADDING, sticky="ew")
        self.user_part.columnconfigure(0, weight=1)

        self.user_box = ctk.CTkTextbox(self.user_part, corner_radius=CORNER_RADIUS, font=FONT)
        self.user_box.grid(column=0, row=0, sticky="ew")
        self.send_button = ctk.CTkButton(self.user_part, text="Send", corner_radius=CORNER_RADIUS, font=FONT, command=controller.button_press)
        self.send_button.grid(column=1, row=0, sticky="", padx=20)

    def get_user_text(self) -> str:
        return self.user_box.get("1.0", "end-1c")