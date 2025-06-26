# 🚦 Pathfinding Grid Simulation

This interactive grid-based pathfinding simulation allows you to visualize pathfinding between a **Start** and **Goal** point, while manually placing **Roads**, **Obstacles**, and **Accidents**. You can also save/load map configurations and reset the grid.

---

## 🧠 Features

- Place Roads, Obstacles, and Accidents using keyboard controls
- Set Start and Goal positions
- Run a simulation to calculate the optimal path
- Save/load your grid configuration
- Reset the grid at any time

---

## 🎮 Controls & Instructions

### 🧱 Setting Grid Elements

| Key | Action                          | Color    |
|-----|----------------------------------|----------|
| `R` | Set current cell to **ROAD**     | Brown    |
| `O` | Set current cell to **OBSTACLE** | Black    |
| `A` | Set current cell to **ACCIDENT** | Red      |

### 🏁 Setting Start and Goal

| Key       | Action                                      | Color     |
|-----------|----------------------------------------------|-----------|
| `S`       | Activate start/goal placement mode           | -         |
| 🖱️ Click  | First click sets **Start** point             | Blue      |
| 🖱️ Click  | Second click sets **Goal** point             | Yellow    |

### 🧭 Running the Simulation

| Key         | Action                                            |
|-------------|---------------------------------------------------|
| `SPACEBAR`  | Runs the simulation from Start to Goal            |
|             | (Make sure both are set before running)           |

### 🧹 Resetting the Grid

| Key | Action                         |
|-----|--------------------------------|
| `C` | Clears the entire grid         |
|     | (Removes all elements & paths) |

### 💾 Saving & Loading Maps

| Key | Action                                                              |
|-----|---------------------------------------------------------------------|
| `W` | Saves current grid config to `map_configuration.txt`               |
| `L` | Loads grid config from `map_configuration.txt`                     |

### ❌ Quitting the Program

- Close the window manually or press the close button

---

## ⚠️ Notes

- You **must set a Start and Goal** before pressing `SPACEBAR` to see the path.
- Obstacles and accidents will affect the pathfinding logic accordingly.

---

## 📁 File Information

- `map_configuration.txt`: Stores saved map layout for reuse.
