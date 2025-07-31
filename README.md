# 🎮 Gesture-Controlled Game Launcher

Control Android games like **Hill Climb Racing** and **Subway Surfers** using your **hand gestures** and a **webcam** — no mouse, no keyboard, just gestures!

This project uses **MediaPipe** for real-time hand tracking and **PyAutoGUI** to trigger keypresses in games running inside **BlueStacks emulator**.

---

## 🕹️ Supported Games

- 🚗 **Hill Climb Racing** – Control the car using gestures:
  - ✋ Open hand → Accelerate (Right arrow)
  - ✊ Closed fist → Brake (Left arrow)

- 🏃 **Subway Surfers** – Control runner using finger count:
  - ☝️ One finger → Left (←)
  - ✌️ Two fingers → Right (→)
  - 🤟 Three fingers → Jump (↑)
  - 🖐️ Four or more → Roll (↓)
  - 🛹 Gesture held → Activates **Hoverboard** (Double press `Space`)

---

## 📸 How It Works

- Uses **your webcam** to detect hand or finger gestures.
- Sends keyboard inputs to the **BlueStacks emulator** running the game.
- You choose which game to play via **command-line menu**.

---

## 🧩 Requirements

- Python 3.8–3.11 (recommended: 3.11)
- Webcam (external or laptop-integrated)
- BlueStacks emulator
- Android games installed in BlueStacks (Hill Climb Racing, Subway Surfers)

---

## 🧰 Installation

### 🔹 Step 1: Clone this repository

```bash
git clone https://github.com/your-username/gesture-game-launcher.git
cd gesture-game-launcher
