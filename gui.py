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