import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class ScenarioEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор сценарію")

        self.data = {
            "character": {"health": 100, "strength": 10, "money": 50},
            "scenes": {}
        }
        self.filename = None

        self.create_menu()
        self.create_tabs()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Новий сценарій", command=self.new_scenario)
        file_menu.add_command(label="Відкрити...", command=self.load_scenario)
        file_menu.add_command(label="Зберегти", command=self.save_scenario)
        file_menu.add_command(label="Зберегти як...", command=self.save_scenario_as)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menu_bar)

    def create_tabs(self):
        self.tabs = ttk.Notebook(self.root)

        self.character_tab = ttk.Frame(self.tabs)
        self.scenario_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.character_tab, text="Персонаж")
        self.tabs.add(self.scenario_tab, text="Сценарій")

        self.tabs.pack(expand=1, fill="both")

        self.create_character_tab()
        self.create_scenario_tab()

    def create_character_tab(self):
        frame = ttk.LabelFrame(self.character_tab, text="Характеристики персонажа")
        frame.pack(padx=10, pady=10, fill="x")

        self.character_fields = {}
        for i, (attr, value) in enumerate(self.data["character"].items()):
            ttk.Label(frame, text=attr.capitalize() + ":").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            var = tk.IntVar(value=value)
            entry = ttk.Entry(frame, textvariable=var, width=10)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.character_fields[attr] = var

        # Додаємо кнопку "Зберегти характеристики"
        ttk.Button(frame, text="Зберегти характеристики", command=self.save_character).grid(row=len(self.data["character"]), column=0, columnspan=2, pady=10)

    def save_character(self):
        """Зберігає змінені характеристики персонажа в self.data."""
        for attr, var in self.character_fields.items():
            self.data["character"][attr] = var.get()
        messagebox.showinfo("Збережено", "Характеристики персонажа збережено!")


    def create_scenario_tab(self):
        self.scene_listbox = tk.Listbox(self.scenario_tab)
        self.scene_listbox.pack(side="left", fill="y", padx=5, pady=5)
        self.scene_listbox.bind("<<ListboxSelect>>", self.load_selected_scene)

        btn_frame = ttk.Frame(self.scenario_tab)
        btn_frame.pack(side="left", fill="y")

        ttk.Button(btn_frame, text="Додати сцену", command=self.add_scene).pack(fill="x", padx=5, pady=2)
        ttk.Button(btn_frame, text="Видалити сцену", command=self.delete_scene).pack(fill="x", padx=5, pady=2)

        self.scene_editor = ttk.Frame(self.scenario_tab)
        self.scene_editor.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.scene_title_var = tk.StringVar()
        ttk.Label(self.scene_editor, text="Назва сцени:").pack(anchor="w")
        self.scene_title_entry = ttk.Entry(self.scene_editor, textvariable=self.scene_title_var)
        self.scene_title_entry.pack(fill="x", padx=5, pady=2)

        ttk.Label(self.scene_editor, text="Текст сцени:").pack(anchor="w")
        self.scene_text = tk.Text(self.scene_editor, height=5)
        self.scene_text.pack(fill="x", padx=5, pady=2)

        self.choices_frame = ttk.LabelFrame(self.scene_editor, text="Варіанти відповідей")
        self.choices_frame.pack(fill="both", padx=5, pady=5, expand=True)
        self.choice_entries = []

        ttk.Button(self.scene_editor, text="Зберегти сцену", command=self.save_scene).pack(fill="x", padx=5, pady=2)

    def add_scene(self):
        new_scene_name = f"Сцена {len(self.data['scenes']) + 1}"
        self.data["scenes"][new_scene_name] = {"text": "", "choices": []}
        self.scene_listbox.insert("end", new_scene_name)

    def delete_scene(self):
        selected = self.scene_listbox.curselection()
        if not selected:
            return
        scene_name = self.scene_listbox.get(selected[0])
        del self.data["scenes"][scene_name]
        self.scene_listbox.delete(selected[0])

    def add_choice_entry(self, text="", next_scene="", effect=None):
        frame = ttk.Frame(self.choices_frame)
        frame.pack(fill="x", padx=5, pady=2)
    
        text_var = tk.StringVar(value=text)
        next_scene_var = tk.StringVar(value=next_scene)
    
        effect = effect or {}
    
        ttk.Entry(frame, textvariable=text_var, width=20).pack(side="left", padx=2)
    
        next_scene_menu = ttk.Combobox(frame, textvariable=next_scene_var, values=list(self.data["scenes"].keys()), width=20, state="readonly")
        next_scene_menu.pack(side="left", padx=2)
    
        char_attr_var = tk.StringVar(value=list(effect.keys())[0] if effect else "")
        char_attr_menu = ttk.Combobox(frame, textvariable=char_attr_var, values=list(self.data["character"].keys()), width=10, state="readonly")
        char_attr_menu.pack(side="left", padx=2)
    
        effect_value_var = tk.StringVar(value=str(list(effect.values())[0]) if effect else "")
        ttk.Entry(frame, textvariable=effect_value_var, width=10).pack(side="left", padx=2)
    
        self.choice_entries.append((text_var, next_scene_var, char_attr_var, effect_value_var))



    def load_selected_scene(self, event):
        selected = self.scene_listbox.curselection()
        if not selected:
            return
    
        scene_name = self.scene_listbox.get(selected[0])
        scene_data = self.data["scenes"][scene_name]
    
        self.scene_title_var.set(scene_name)
        self.scene_text.delete("1.0", "end")
        self.scene_text.insert("1.0", scene_data["text"])
    
        # Очищення старих варіантів відповідей
        for widget in self.choices_frame.winfo_children():
            widget.destroy()
    
        self.choice_entries = []
    
        for choice in scene_data["choices"]:
            effect = choice.get("effect", {})
            attr, value = (next(iter(effect.items())) if effect else ("", ""))  # Розбираємо словник ефекту
            self.add_choice_entry(choice["text"], choice["next_scene"], attr, str(value))

    
        ttk.Button(self.choices_frame, text="Додати відповідь", command=self.add_choice_entry).pack(fill="x", padx=5, pady=2)
    

    def add_choice_entry(self, text="", next_scene="", attr="", effect_value=""):
        frame = ttk.Frame(self.choices_frame)
        frame.pack(fill="x", padx=5, pady=2)
    
        text_var = tk.StringVar(value=text)
        next_scene_var = tk.StringVar(value=next_scene)
        char_attr_var = tk.StringVar(value=attr)  # Змінювана характеристика
        effect_value_var = tk.StringVar(value=effect_value)  # Значення ефекту
    
        ttk.Entry(frame, textvariable=text_var, width=20).pack(side="left", padx=2)
        next_scene_menu = ttk.Combobox(frame, textvariable=next_scene_var, values=list(self.data["scenes"].keys()), width=20, state="readonly")
        next_scene_menu.pack(side="left", padx=2)
        char_attr_menu = ttk.Combobox(frame, textvariable=char_attr_var, values=list(self.data["character"].keys()), width=10, state="readonly")
        char_attr_menu.pack(side="left", padx=2)
        ttk.Entry(frame, textvariable=effect_value_var, width=10).pack(side="left", padx=2)
    
        self.choice_entries.append((text_var, next_scene_var, char_attr_var, effect_value_var))
    

    def save_scene(self):
        old_scene_name = self.scene_listbox.get(self.scene_listbox.curselection()) if self.scene_listbox.curselection() else None
        new_scene_name = self.scene_title_var.get().strip()
        
        if not new_scene_name:
            messagebox.showwarning("Помилка", "Назва сцени не може бути порожньою!")
            return
        
        # Видаляємо стару сцену, якщо змінилася назва
        if old_scene_name and old_scene_name != new_scene_name:
            self.data["scenes"].pop(old_scene_name, None)
            self.scene_listbox.delete(self.scene_listbox.get(0, "end").index(old_scene_name))
        
        # Оновлюємо дані сцени
        self.data["scenes"][new_scene_name] = {
            "text": self.scene_text.get("1.0", "end").strip(),
            "choices": [
                {
                    "text": text.get(),
                    "next_scene": next_scene.get(),
                    "effect": {char_attr.get(): int(effect_value.get())} if char_attr.get() else {}
                }
                for text, next_scene, char_attr, effect_value in self.choice_entries
            ],
        }
    
        # Оновлюємо список сцен у Listbox
        if new_scene_name not in self.scene_listbox.get(0, "end"):
            self.scene_listbox.insert("end", new_scene_name)
    
    
    def new_scenario(self):
        self.data = {"character": {"health": 100, "strength": 10, "money": 50}, "scenes": {}}
        self.scene_listbox.delete(0, "end")

    def save_scenario(self):
        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Збережено", f"Сценарій збережено у {self.filename}!")
        else:
            self.save_scenario_as()

    def save_scenario_as(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON файли", "*.json")])
        if filename:
            self.filename = filename
            self.save_scenario()

    def update_ui_after_load(self):
        # Оновлення характеристик персонажа
        for attr, var in self.character_fields.items():
            if attr in self.data["character"]:
                var.set(self.data["character"][attr])
    
        # Очищення списку сцен
        self.scene_listbox.delete(0, "end")
    
        # Додавання сцен у список
        for scene_name in self.data["scenes"]:
            self.scene_listbox.insert("end", scene_name)
    
        # Очищення полів редагування сцени
        self.scene_title_var.set("")
        self.scene_text.delete("1.0", "end")
    
        # Очищення варіантів відповідей
        for widget in self.choices_frame.winfo_children():
            widget.destroy()
    
        self.choice_entries = []
    

    def load_scenario(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON файли", "*.json")])
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.filename = filename
            self.update_ui_after_load()
            messagebox.showinfo("Завантажено", f"Сценарій завантажено з {filename}!")


root = tk.Tk()
app = ScenarioEditor(root)
root.mainloop()
