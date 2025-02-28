import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Scrollbar, Toplevel
import json
import networkx as nx

class ScenarioVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Візуалізатор сценарію")
        self.root.geometry("400x200")
        
        tk.Button(self.root, text="Завантажити сценарій", command=self.load_scenario, font=("Arial", 12)).pack(pady=20)
        
    def load_scenario(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON файли", "*.json")])
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.open_graph_window()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити сценарій: {e}")
    
    def open_graph_window(self):
        self.graph_window = Toplevel(self.root)
        self.graph_window.title("Граф сценарію")
        self.graph_window.geometry("1200x800")
        
        self.canvas_frame = tk.Frame(self.graph_window)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 2000, 2000))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scroll_x = Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.scroll_y = Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_node)
        
        self.draw_graph()
    
    def draw_graph(self):
        self.G = nx.DiGraph()
        self.pos = {}
        self.node_items = {}
        self.node_dragging = None
        self.canvas.delete("all")
        
        if "scenes" not in self.data:
            messagebox.showerror("Помилка", "Некоректний формат JSON-файлу!")
            return
        
        scenes = self.data["scenes"]
        
        for scene_id, scene in scenes.items():
            text = scene.get("text", "Без назви")
            self.G.add_node(scene_id, label=text)
            
            for choice in scene.get("choices", []):
                edge_label = choice.get("text", "")
                
                effects = [f"{attr}: {choice[attr]}" for attr in ["health", "strength", "money"] if attr in choice]
                
                if effects:
                    edge_label += " (" + ", ".join(effects) + ")"
                
                self.G.add_edge(scene_id, choice["next_scene"], label=edge_label)
        
        self.pos = nx.spring_layout(self.G, seed=42, k=0.8, scale=800)
        
        for node, (x, y) in self.pos.items():
            x, y = x + 1000, y + 800  # Підняв граф трохи вище
            node_id = self.canvas.create_oval(x-40, y-40, x+40, y+40, fill="#A3BE8C", tags=("node", node))
            text_id = self.canvas.create_text(x, y, text=self.G.nodes[node].get('label', node), width=80, justify=tk.CENTER, tags=("text", node))
            self.node_items[node] = (node_id, text_id)
        
        self.draw_edges()
    
    def draw_edges(self):
        self.canvas.delete("edge")
        for edge in self.G.edges:
            x1, y1 = self.pos[edge[0]]
            x2, y2 = self.pos[edge[1]]
            x1, y1, x2, y2 = x1 + 1000, y1 + 800, x2 + 1000, y2 + 800
            
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, arrowshape=(20, 24, 8), fill="#D08770", width=3, tags="edge")
            
            label = self.G.edges[edge].get("label", "")
            if label:
                label_x = (x1 + x2) / 2
                label_y = (y1 + y2) / 2
                self.canvas.create_text(label_x, label_y, text=label, font=("Arial", 10), width=100, tags="edge")
    
    def start_drag(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        
        if "node" in tags:
            self.node_dragging = tags[1]
            self.drag_offset_x = event.x
            self.drag_offset_y = event.y
    
    def drag_node(self, event):
        if self.node_dragging:
            dx = event.x - self.drag_offset_x
            dy = event.y - self.drag_offset_y
            
            node_id, text_id = self.node_items[self.node_dragging]
            self.canvas.move(node_id, dx, dy)
            self.canvas.move(text_id, dx, dy)
            
            x, y = self.pos[self.node_dragging]
            self.pos[self.node_dragging] = (x + dx, y + dy)
            
            self.drag_offset_x = event.x
            self.drag_offset_y = event.y
            self.draw_edges()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScenarioVisualizer(root)
    root.mainloop()
