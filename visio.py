import json
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox

class ScenarioVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Приховуємо головне вікно Tkinter
        self.json_file = self.select_file()
        
        if not self.json_file:
            return
        
        self.data = self.load_scenario()
        if not self.data:
            return
        
        self.G = nx.DiGraph()
        self.pos = {}
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

    def select_file(self):
        """Відкриває діалог вибору JSON-файлу."""
        file_path = filedialog.askopenfilename(
            title="Select a JSON Scenario File",
            filetypes=[("JSON files", "*.json")]
        )
        return file_path

    def load_scenario(self):
        """Завантажує та перевіряє JSON-файл."""
        if not self.json_file:
            messagebox.showwarning("Warning", "No file selected!")
            return None

        try:
            with open(self.json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Валідація структури JSON
            if "character" not in data or "scenes" not in data:
                raise ValueError("Invalid JSON format: Missing 'character' or 'scenes' key.")

            if not isinstance(data["scenes"], dict):
                raise ValueError("Invalid JSON format: 'scenes' should be a dictionary.")

            for scene_id, scene in data["scenes"].items():
                if "text" not in scene or "choices" not in scene:
                    raise ValueError(f"Scene '{scene_id}' is missing 'text' or 'choices' keys.")

                for choice in scene["choices"]:
                    if "text" not in choice or "next_scene" not in choice:
                        raise ValueError(f"Choice in scene '{scene_id}' is missing 'text' or 'next_scene'.")

            return data
        
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file format!")
            return None
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return None

    def build_graph(self):
        """Створює граф із сцен."""
        scenes = self.data["scenes"]

        # Додаємо вузли (сцени)
        for scene_id in scenes:
            self.G.add_node(scene_id, label=scene_id)

        # Додаємо стрілки (зв’язки між сценами)
        for scene_id, scene_data in scenes.items():
            for choice in scene_data["choices"]:
                next_scene = choice["next_scene"]
                if next_scene in scenes:
                    self.G.add_edge(scene_id, next_scene, label=choice["text"])

    def draw_graph(self):
        """Малює граф із стрілками."""
        self.ax.clear()
        self.pos = nx.spring_layout(self.G, seed=42, k=1.2)

        # Малюємо вузли (сцени)
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color="lightblue", node_size=2000)

        # Малюємо зв’язки (орієнтовані стрілки)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color="black", arrows=True, arrowsize=20)

        # Додаємо підписи сцен
        labels = {node: node for node in self.G.nodes}
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, labels=labels, font_size=10, font_weight="bold")

        # Додаємо підписи до стрілок (текст вибору)
        edge_labels = {(u, v): data["label"] for u, v, data in self.G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.G, self.pos, ax=self.ax, edge_labels=edge_labels, font_size=9, label_pos=0.5)

        # Додаємо стрілки червоного кольору з напрямком
        for edge in self.G.edges:
            x1, y1 = self.pos[edge[0]]
            x2, y2 = self.pos[edge[1]]
            self.ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="red", lw=2)
            )

        self.ax.set_title("Scenario Graph Visualization")
        self.ax.axis("off")  # Вимикаємо координатні осі
        self.fig.canvas.draw()

    def on_scroll(self, event):
        """Масштабування графа колесом миші."""
        scale_factor = 1.1 if event.step > 0 else 0.9
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([x * scale_factor for x in xlim])
        self.ax.set_ylim([y * scale_factor for y in ylim])
        self.fig.canvas.draw()

    def run(self):
        """Запускає візуалізацію."""
        if not self.data:
            return
        
        self.build_graph()
        self.draw_graph()

        # Додаємо обробник масштабування
        self.fig.canvas.mpl_connect("scroll_event", self.on_scroll)

        plt.show()

# Запуск програми
if __name__ == "__main__":
    visualizer = ScenarioVisualizer()
    visualizer.run()
