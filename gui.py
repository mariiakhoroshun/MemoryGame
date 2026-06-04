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

    def show_game_screen(self):
        self.clear_window()
        top_panel = tk.Frame(self.main_frame, bg=self.bg_color)
        top_panel.pack(pady=10)
        self.timer_label = tk.Label(top_panel, text="Час: 0 с", font=("Arial", 14), bg=self.bg_color)
        self.timer_label.grid(row=0, column=0, padx=10)
        self.score_label = tk.Label(top_panel, text="Відкрито пар: 0 | Залишилось: 0 | Ходів: 0", font=("Arial", 14), bg=self.bg_color)
        self.score_label.grid(row=0, column=1, padx=10)
        self.pause_button = tk.Button(top_panel, text="Пауза", font=("Arial", 12), command=self.toggle_pause)
        self.pause_button.grid(row=0, column=2, padx=10)
        menu_button = tk.Button(top_panel, text="Меню", font=("Arial", 12), command=self.back_to_menu)
        menu_button.grid(row=0, column=3, padx=10)
        bg_button = tk.Button(top_panel, text="Змінити фон", font=("Arial", 12), command=self.show_background_menu)
        bg_button.grid(row=0, column=4, padx=10)
        self.cards_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.cards_frame.pack(pady=20)
        self.create_card_buttons()
        self.update_score()

    def create_card_buttons(self):
        for index, card in enumerate(self.game.cards):
            row = index // self.game.cols
            col = index % self.game.cols
            button = tk.Button(self.cards_frame, text="?", font=("Arial", 20, "bold"), width=4, height=2, bg="#f5a623", command=lambda i=index: self.card_click(i))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)

    def card_click(self, index):
        if self.is_paused:
            return
        opened = self.game.open_card(index)
        if not opened:
            return
        self.update_card_button(index)
        if len(self.game.opened_cards) == 2:
            result = self.game.check_pair()
            self.update_score()
            if result is True:
                self.update_all_buttons()
                if self.game.is_game_finished:
                    self.finish_game()
            elif result is False:
                self.root.after(800, self.close_wrong_pair)

    def update_card_button(self, index):
        card = self.game.get_card(index)
        button = self.buttons[index]

        if card.is_open or card.is_matched:
            img_path = card.value
            if img_path not in self.loaded_images:
                try:
                    pil_img = Image.open(img_path).resize((80, 80))
                    self.loaded_images[img_path] = ImageTk.PhotoImage(pil_img)
                except Exception:
                    self.loaded_images[img_path] = None

            img = self.loaded_images[img_path]

            if card.is_matched:
                bg_color = "#7bed9f"
                state = "disabled"
            else:
                bg_color = "#7ed6df"
                state = "normal"

            if img:
                button.config(image=img, text="", width=100, height=100, bg=bg_color, state=state)
            else:
                button.config(image="", text="X", width=4, height=2, bg=bg_color, state=state)
        else:
            button.config(image="", text="?", width=4, height=2, bg="#f5a623", state="normal")

    def update_all_buttons(self):
        for index in range(len(self.buttons)):
            self.update_card_button(index)

    def close_wrong_pair(self):
        self.game.close_unmatched_cards()
        self.update_all_buttons()

    def update_score(self):
        opened = self.game.get_opened_pairs_count()
        closed = self.game.get_closed_pairs_count()
        moves = self.game.get_moves_count()
        self.score_label.config(text=f"Відкрито пар: {opened} | Залишилось: {closed} | Ходів: {moves}")

    def update_timer(self):
        if self.timer_running and not self.is_paused:
            self.timer_label.config(text=f"Час: {self.seconds} с")
            self.seconds += 1
            self.root.after(1000, self.update_timer)

    def toggle_pause(self):
        if self.game is None:
            return
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.timer_running = False
            self.pause_button.config(text="Продовжити")
            for button in self.buttons:
                button.config(state="disabled")
        else:
            self.timer_running = True
            self.pause_button.config(text="Пауза")
            self.update_all_buttons()
            self.update_timer()

    def finish_game(self):
        self.timer_running = False
        messagebox.showinfo("Перемога!", f"Вітаю! Ви відкрили всі пари.\nВаш час: {self.seconds - 1} с\nКількість ходів: {self.game.get_moves_count()}")

    def back_to_menu(self):
        self.timer_running = False
        self.is_paused = False
        self.show_menu()

    def show_background_menu(self):
        bg_window = tk.Toplevel(self.root)
        bg_window.title("Зміна фону")
        bg_window.geometry("300x250")
        label = tk.Label(bg_window, text="Оберіть колір фону:", font=("Arial", 14))
        label.pack(pady=15)
        colors = [("Блакитний", "#dceefb"), ("Рожевий", "#ffe0f0"), ("Зелений", "#e0ffe0"), ("Жовтий", "#fff5cc"), ("Сірий", "#eeeeee")]
        for color_name, color_code in colors:
            button = tk.Button(bg_window, text=color_name, font=("Arial", 12), width=20, command=lambda c=color_code, w=bg_window: self.set_game_background(c, w))
            button.pack(pady=5)

    def set_game_background(self, color, window):
        self.bg_color = color
        self.main_frame.config(bg=self.bg_color)
        self.cards_frame.config(bg=self.bg_color)
        for widget in self.main_frame.winfo_children():
            try:
                widget.config(bg=self.bg_color)
            except tk.TclError:
                pass
        window.destroy()