# 🤖 **Dynamic A* Pathfinding Simulation - No Stuck Guarantee*\* 🚀

Welcome to an interactive simulation where **pathfinding meets unpredictability**! This project uses the powerful **Dynamic A\* (D-star)** algorithm to help a robot 🦾 navigate through a grid filled with **random obstacles**. The catch? **Obstacles appear dynamically** while the robot is moving, forcing it to adapt its path in real-time! 😱

## 🔍 **Features:**

* **🔄 Dynamic Obstacle Generation**: Watch as obstacles are added randomly on the grid while the robot is on its path. Will it get stuck? 🤔 No, because the path is recalculated as needed!
* **🧭 D* Pathfinding*\*: The robot uses the **D* algorithm*\* with a **Manhattan heuristic** to find the optimal path from the start to the goal. Fast and efficient! ⚡
* **🎮 Real-time Visualization**: Pygame brings the action to life, showing the grid, robot movement, pathfinding steps, obstacles, and more!
* **📊 Info Panel**: Get live updates on:

  * 🪜 Steps taken
  * 🚧 Obstacles added
  * ⏳ Elapsed time
* **🎯 Goal Reached**: See the robot reach its destination with a message of success when it finally gets there! 🎉

## 🛠 **How It Works:**

1. The robot starts at the top-left corner of the grid.
2. The robot calculates its path using the D\* algorithm to reach the goal at the bottom-right.
3. Random obstacles 🟫 are added periodically, forcing the robot to recalculate its path.
4. Watch as the robot adapts in real-time to reach its destination without getting stuck!

## 🔧 **Technologies Used:**

* **Python** 🐍
* **Pygame** 🎮
* **D* Pathfinding Algorithm*\* 💡

## 🏃‍♂️ **Run It Locally**:

1. Clone this repo:

   ```bash
   git clone https://github.com/yourusername/dynamic-pathfinding.git
   ```
2. Install the dependencies:

   ```bash
   pip install pygame
   ```
3. Run the script:

   ```bash
   python pathfinding_simulation.py
   ```

## ✨ **Contribute**:

Feel free to fork the repo, open issues, and submit pull requests. If you have ideas to make it even more dynamic or fun, I’d love to hear them! 💬

---

This version should capture the attention of potential users or contributors, making it both informative and fun!
