# Interactive Story Toolkit

Interactive Story Toolkit is a set of three applications designed to help you create, edit, play, and visualize interactive story scenarios. It includes a **Scenario Editor**, a **Game Player**, and a **Scenario Visualizer**.

## Features
- **Scenario Editor** (`plot_editor.py`): Create and manage story scenarios with scenes, choices, and character attributes.
- **Game Player** (`plot_game.py`): Play through interactive scenarios with character progression and choices.
- **Scenario Visualizer** (`visio.py`): View the story structure as a connected graph.

---

## Installation
1. Ensure you have Python 3 installed.
2. Install required dependencies:
   ```sh
   pip install networkx
# How to Use

## 📜 Scenario Editor (plot_editor.py)
The Scenario Editor allows you to create and modify interactive story scenarios.

### Steps:
- Create a new scenario or open an existing one (.json format).
- Edit character attributes (e.g., health, strength, money).
- Create scenes with descriptions and multiple choices.
- Define choices leading to other scenes, with optional effects on character attributes.
- Save the scenario to use in the Game Player.

## 🎮 Game Player (plot_game.py)
The Game Player lets you experience your interactive story.

### Steps:
- Load a scenario (.json file).
- Enter your character’s name and start playing.
- Make choices to navigate through the story.
- Character attributes change based on choices.
- Game ends when the story reaches a final scene or the character’s health reaches zero.

## 🌐 Scenario Visualizer (visio.py)
The Scenario Visualizer helps you see the structure of your story as a graph.

### Steps:
- Load a scenario (.json file).
- View the graph representation of the story.
- Nodes represent scenes, and arrows show transitions between them.
- Drag nodes to adjust the view.

## File Format (JSON)
Scenarios are saved as `.json` files with the following structure:

```json
{
    "character": {
        "health": 100,
        "strength": 10,
        "money": 50
    },
    "scenes": {
        "scene1": {
            "text": "You wake up in a dark forest...",
            "choices": [
                {
                    "text": "Go left",
                    "next_scene": "scene2",
                    "effect": {"health": -10}
                },
                {
                    "text": "Go right",
                    "next_scene": "scene3"
                }
            ]
        }
    }
}
