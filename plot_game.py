import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Гра")
        self.root.geometry("500x500")
        self.root.configure(bg="#2E3440")  # Темний фон

        self.data = {}
        self.character = {}
        self.current_scene = None
        self.player_name = ""

        self.create_styles()
        self.create_ui()

    def create_styles(self):
        """Налаштування стилю інтерфейсу"""
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=6)
        style.configure("TLabel", font=("Arial", 12), background="#2E3440", foreground="white", wraplength=450)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"), background="#2E3440", foreground="white")

    def create_ui(self):
        """Створення графічного інтерфейсу"""
        ttk.Button(self.root, text="Завантажити сценарій", command=self.load_scenario).pack(pady=10)

        self.name_frame = ttk.Frame(self.root, style="TFrame")
        self.name_frame.pack()
        ttk.Label(self.name_frame, text="Ваше ім'я:", style="Header.TLabel").pack(side="left", padx=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.name_frame, textvariable=self.name_var, font=("Arial", 12), width=15)
        self.name_entry.pack(side="left")
        ttk.Button(self.name_frame, text="Почати гру", command=self.start_game).pack(side="left", padx=5)

        self.text_label = ttk.Label(self.root, text="", justify="left", wraplength=450, font=("Arial", 12))
        self.text_label.pack(pady=15)

        self.choices_frame = ttk.Frame(self.root, style="TFrame")
        self.choices_frame.pack()

        self.character_label = ttk.Label(self.root, text="", font=("Arial", 12, "italic"), foreground="#A3BE8C")
        self.character_label.pack(pady=10)

    def load_scenario(self):
        """Завантаження сценарію гри"""
        filename = filedialog.askopenfilename(filetypes=[("JSON файли", "*.json")])
        if not filename:
            return
        with open(filename, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.character = self.data.get("character", {}).copy()  # Створюємо копію характеристик
        messagebox.showinfo("Готово", "Сценарій завантажено!")

    def start_game(self):
        """Запуск гри"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Помилка", "Введіть ім'я персонажа!")
            return

        self.player_name = name  # Зберігаємо ім'я персонажа
        self.current_scene = list(self.data.get("scenes", {}).keys())[0]
        self.name_entry.config(state="disabled")  # Блокуємо поле імені після старту гри
        self.update_scene()

    def update_scene(self):
        """Оновлення сцени"""
        if not self.current_scene or self.current_scene not in self.data["scenes"]:
            return
        scene = self.data["scenes"][self.current_scene]

        # Анімація поступового виведення тексту
        self.animate_text(scene["text"])

        for widget in self.choices_frame.winfo_children():
            widget.destroy()

        if not scene["choices"]:  # Якщо немає вибору - це фінальна сцена
            self.root.after(2000, lambda: self.end_game(scene["text"]))  # Даємо час дочитати сцену
        else:
            for choice in scene["choices"]:
                btn = ttk.Button(self.choices_frame, text=choice["text"], 
                                 command=lambda ch=choice: self.make_choice(ch))
                btn.pack(fill="x", pady=3, padx=10)

        self.character_label.config(text=self.format_characteristics())

    def animate_text(self, text, index=0):
        """Анімація поступового виведення тексту"""
        if index == 0:
            self.text_label.config(text="")  # Очистка перед виведенням нового тексту

        if index < len(text):
            self.text_label.config(text=self.text_label["text"] + text[index])
            self.root.after(30, lambda: self.animate_text(text, index + 1))  # Швидкість друку
        else:
            return

    def make_choice(self, choice):
        """Обробка вибору гравця"""
        if "effect" in choice:
            for attr, value in choice["effect"].items():
                if attr in self.character:
                    self.character[attr] += value
    
        # Перевіряємо, чи здоров'я впало до 0 або нижче
        if self.character.get("health", 1) <= 0:
            messagebox.showinfo("Гра закінчена", "Ви програли! 💀")
            self.root.quit()
            return
    
        self.current_scene = choice["next_scene"]
    
        if not self.current_scene:
            self.end_game(self.data["scenes"][choice["next_scene"]]["text"])
        else:
            self.update_scene()

    def format_characteristics(self):
        """Форматування характеристик героя"""
        formatted_text = f"🎭 {self.player_name} – Характеристики:\n"
        for key, value in self.character.items():
            formatted_text += f"🔹 {key.capitalize()}: {value}\n"
        return formatted_text

    def end_game(self, final_text):
        """Завершення гри: показ фінальної сцени та характеристик"""
        final_message = f"{final_text}\n\n🔥 Фінальні характеристики {self.player_name}:\n{self.format_characteristics()}"
        messagebox.showinfo("Кінець гри", final_message)
        self.root.quit()  # Закриття гри

root = tk.Tk()
app = Game(root)
root.mainloop()
