import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from game_logic import MemoryGame

class MemoryGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Гра тренування пам'яті")
        self.root.geometry("750x650")
        self.bg_color = "#dceefb"
        self.game = None
        self.buttons = []
        self.seconds = 0
        self.timer_running = False
        self.is_paused = False
        self.loaded_images = {}
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill="both", expand=True)
        self.show_menu()

    def clear_window(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_window()
        title = tk.Label(self.main_frame, text="Гра тренування пам'яті", font=("Arial", 28, "bold"), bg=self.bg_color)
        title.pack(pady=40)
        subtitle = tk.Label(self.main_frame, text="Оберіть рівень складності:", font=("Arial", 18), bg=self.bg_color)
        subtitle.pack(pady=20)
        very_easy_button = tk.Button(self.main_frame, text="Дуже легкий рівень: 2 x 3", font=("Arial", 16), width=25, command=lambda: self.start_game(2, 3))
        very_easy_button.pack(pady=10)
        easy_button = tk.Button(self.main_frame, text="Легкий рівень: 4 x 4", font=("Arial", 16), width=25, command=lambda: self.start_game(4, 4))
        easy_button.pack(pady=10)
        medium_button = tk.Button(self.main_frame, text="Середній рівень: 4 x 6", font=("Arial", 16), width=25, command=lambda: self.start_game(4, 6))
        medium_button.pack(pady=10)
        hard_button = tk.Button(self.main_frame, text="Складний рівень: 6 x 6", font=("Arial", 16), width=25, command=lambda: self.start_game(6, 6))
        hard_button.pack(pady=10)
        bg_label = tk.Label(self.main_frame, text="Колір фону:", font=("Arial", 16), bg=self.bg_color)
        bg_label.pack(pady=20)
        colors_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        colors_frame.pack()
        colors = [("Блакитний", "#dceefb"), ("Рожевий", "#ffe0f0"), ("Зелений", "#e0ffe0"), ("Жовтий", "#fff5cc"), ("Сірий", "#eeeeee")]
        for color_name, color_code in colors:
            button = tk.Button(colors_frame, text=color_name, font=("Arial", 12), command=lambda c=color_code: self.change_background(c))
            button.pack(side="left", padx=5)

    def change_background(self, color):
        self.bg_color = color
        self.main_frame.config(bg=self.bg_color)
        for widget in self.main_frame.winfo_children():
            try:
                widget.config(bg=self.bg_color)
            except tk.TclError:
                pass

    def start_game(self, rows, cols):
        self.game = MemoryGame(rows, cols)
        self.buttons = []
        self.seconds = 0
        self.timer_running = True
        self.is_paused = False
        self.show_game_screen()
        self.update_timer()