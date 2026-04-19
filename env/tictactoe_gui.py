import tkinter as tk
from tkinter import font as tkfont

class TicTacToeGUI:
    def __init__(self, agent, env_class, size, win_length):
        self.agent = agent
        self.size = size
        # Assuming your environment handles the logic for size/win_length
        self.env = env_class(board_size=size, win_length=win_length)
        
        self.window = tk.Tk()
        self.window.title(f"Tic Tac Toe {size}x{size} ({win_length} in-a-row)")

        # --- DYNAMIC SCALING CALCULATIONS ---
        # Scale the UI so a 6x6 doesn't take up the whole screen
        base_size = 600  # Target window dimension
        cell_size = base_size // size
        
        # Adjust font size: 32 for 3x3, 16 for 6x6
        dynamic_font_size = max(12, int(96 / size)) 
        # Adjust button padding/dimensions
        btn_w = max(2, int(16 / size))
        btn_h = max(1, int(6 / size))
        
        # COLORS
        self.COLOR_BG = "#2C3E50"
        self.COLOR_GRID = "#34495E"
        self.COLOR_X = "#3498DB"
        self.COLOR_O = "#E74C3C"
        self.COLOR_HOVER = "#3E5871"
        self.COLOR_TEXT_LIGHT = "#ECF0F1"

        self.window.configure(bg=self.COLOR_BG)
        self.buttons = []

        self.game_font = tkfont.Font(family="Helvetica", size=dynamic_font_size, weight="bold")
        self.status_font = tkfont.Font(family="Helvetica", size=12)

        self.main_frame = tk.Frame(self.window, bg=self.COLOR_BG, padx=20, pady=20)
        self.main_frame.pack()

        # Pass scaling params to board builder
        self._build_board(btn_w, btn_h)
        self._build_status()

        self.window.mainloop()

    def _build_board(self, w, h):
        self.board_frame = tk.Frame(self.main_frame, bg=self.COLOR_GRID)
        self.board_frame.pack()

        for i in range(self.size * self.size):
            btn = tk.Button(
                self.board_frame,
                text=" ",
                font=self.game_font,
                width=w, # Scaled width
                height=h, # Scaled height
                bg=self.COLOR_BG,
                fg=self.COLOR_TEXT_LIGHT,
                relief="flat",
                borderwidth=0,
                activebackground=self.COLOR_BG,
                command=lambda i=i: self.human_move(i)
            )

            btn.grid(row=i // self.size, column=i % self.size, padx=1, pady=1)
            btn.bind("<Enter>", lambda e, b=btn: self._hover(b))
            btn.bind("<Leave>", lambda e, b=btn: self._leave(b))

            self.buttons.append(btn)

    def _build_status(self):
        self.status = tk.Label(
            self.main_frame,
            text="Your turn (X)",
            bg=self.COLOR_BG,
            fg=self.COLOR_X,
            font=self.status_font
        )
        self.status.pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Restart",
            command=self.reset_game,
            bg="#95A5A6",
            fg="white",
            relief="flat",
            padx=10,
            pady=5
        ).pack()

    # --- HOVER & GAME LOGIC (Remains similar but ensures reliability) ---

    def _hover(self, btn):
        idx = self.buttons.index(btn)
        if self.env.board[idx] == 0 and not self.env.done:
            btn["bg"] = self.COLOR_HOVER

    def _leave(self, btn):
        btn["bg"] = self.COLOR_BG

    def human_move(self, i):
        if self.env.done or self.env.board[i] != 0:
            return

        self.env.step(i, 1)
        self.update_board()

        if self.env.done:
            self.end_game()
            return

        self.status["text"] = "AI thinking..."
        self.status["fg"] = self.COLOR_TEXT_LIGHT
        self.window.after(200, self.ai_move)

    def ai_move(self):
        if self.env.done: return
        
        # Use a copy to prevent accidental state mutation
        state = self.env.board.copy()
        action = self.agent.act(state, self.env.available_actions())

        self.env.step(action, -1)
        self.update_board()

        if self.env.done:
            self.end_game()
        else:
            self.status["text"] = "Your turn (X)"
            self.status["fg"] = self.COLOR_X

    def update_board(self):
        symbols = {1: "X", -1: "O", 0: " "}
        colors = {1: self.COLOR_X, -1: self.COLOR_O, 0: self.COLOR_TEXT_LIGHT}

        for i, b in enumerate(self.buttons):
            val = self.env.board[i]
            b["text"] = symbols[val]
            b["fg"] = colors[val]
            b["bg"] = self.COLOR_BG

    def end_game(self):
        if self.env.winner == 1:
            self.status["text"] = "You Win!"
            self.status["fg"] = "#2ECC71"
        elif self.env.winner == -1:
            self.status["text"] = "AI Wins!"
            self.status["fg"] = self.COLOR_O
        else:
            self.status["text"] = "Draw!"
            self.status["fg"] = self.COLOR_TEXT_LIGHT

    def reset_game(self):
        self.env.reset()
        self.update_board()
        self.status["text"] = "Your turn (X)"
        self.status["fg"] = self.COLOR_X

def run_gui(agent, env_class, size=6, win_length=4):
    TicTacToeGUI(agent, env_class, size, win_length)
