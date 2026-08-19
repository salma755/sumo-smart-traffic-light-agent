# 🚦 Smart Traffic Light Control using Deep Q-Learning (DQN) & SUMO

An AI-driven traffic management system that learns to optimize traffic signal control at urban intersections using **Deep Q-Networks (DQN)** with **PyTorch**, integrated with the **SUMO (Simulation of Urban MObility)** traffic simulator through **TraCI**.

The system uses Reinforcement Learning to learn traffic-light policies that aim to reduce **vehicle waiting time, queue formation, and overall traffic congestion**.

---

https://github.com/user-attachments/assets/c242069e-c2da-4286-8dae-d6fa486cd0b8

## 📌 Overview

Traditional traffic-light systems commonly rely on fixed timing plans. These plans may not respond effectively to changing traffic conditions.

This project applies **Deep Reinforcement Learning** to allow an agent to interact with a simulated traffic environment and learn which traffic signal phase should be selected based on the current traffic state.

The main components are:

* **SUMO** — Traffic simulation environment
* **TraCI** — Communication interface between Python and SUMO
* **DQN Agent** — Learns the optimal traffic-light policy
* **PyTorch MLP** — Approximates the Q-function
* **Experience Replay** — Stabilizes training
* **ε-greedy Exploration** — Balances exploration and exploitation

---

## 🧠 System Architecture

```text
                    ┌─────────────────────┐
                    │        SUMO         │
                    │ Traffic Simulation  │
                    └──────────┬──────────┘
                               │
                             TraCI
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Environment       │
                    │       env.py        │
                    └──────────┬──────────┘
                               │
                          State (Sₜ)
                               │
                               ▼
                    ┌─────────────────────┐
                    │     DQN Agent       │
                    │      agent.py       │
                    └──────────┬──────────┘
                               │
                         Action (Aₜ)
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Traffic Light      │
                    │     Control         │
                    └──────────┬──────────┘
                               │
                         Reward (Rₜ)
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Replay Memory      │
                    │     memory.py       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   PyTorch MLP       │
                    │      model.py       │
                    └─────────────────────┘
```

---

##  Objective

The objective is to learn a traffic signal control policy that minimizes traffic congestion.

The agent receives information about the current traffic situation, selects a traffic-light phase, observes the resulting traffic conditions, and receives a reward.

The learning process follows:

```text
State → Action → Environment → Reward → Next State
```

---

##  Methodology

### 1. State Representation

The traffic state is represented using an **80-element vector**.

The intersection is divided into spatial cells across different lane groups. Each cell contains information about vehicles based on their traffic conditions, including whether vehicles are moving or stationary according to predefined speed thresholds.

The resulting vector is used as the input to the DQN.

```text
Traffic Environment
        │
        ▼
Lane Groups
        │
        ▼
Spatial Cells
        │
        ▼
80-Dimensional State Vector
        │
        ▼
DQN
```

---

### 2. Action Space

The agent has **4 discrete actions** corresponding to the primary traffic-light phases.

These actions control the main North-South and East-West traffic flows, including dedicated left-turn phases.

```text
Action 0 → Traffic Phase 1
Action 1 → Traffic Phase 2
Action 2 → Traffic Phase 3
Action 3 → Traffic Phase 4
```

The exact phase mapping is defined in `constants.py`.

---

### 3. Reward Function

The reward function is designed to penalize traffic congestion.

The implemented reward is:

```text
R = -(waiting_time + 15.0 × queue_length)
```

Where:

* `waiting_time` represents cumulative vehicle waiting time.
* `queue_length` represents the number of queued vehicles.
* `15.0` is the queue-length weighting factor.

Therefore, lower congestion results in a better reward.

---

## 🤖 Deep Q-Network

The project uses a **Deep Q-Network (DQN)** implemented with PyTorch.

The neural network approximates the Q-value function:

```text
Q(s, a)
```

where:

* `s` = current traffic state
* `a` = selected traffic-light action

The model is implemented in:

```text
model.py
```

The network receives the 80-dimensional traffic state and produces Q-values for the four available actions.

```text
80 State Features
       │
       ▼
   MLP Network
       │
       ▼
4 Q-Values
       │
       ▼
Best Action
```

---

## 🔄 Experience Replay

The agent uses an **Experience Replay Memory** to improve training stability.

Each experience is stored as:

```text
(state, action, reward, next_state)
```

Experiences are stored in a replay buffer and sampled during training.

This reduces the correlation between consecutive experiences and allows the agent to learn from previously observed traffic situations.

The implementation is located in:

```text
memory.py
```

---

## 🎲 ε-Greedy Exploration

The agent uses an **ε-greedy strategy**.

At the beginning of training, the agent explores different actions more frequently.

As training progresses, ε decreases, causing the agent to rely increasingly on the actions predicted by the DQN.

```text
High ε
  │
  ▼
More Exploration
  │
  ▼
Training
  │
  ▼
Lower ε
  │
  ▼
More Exploitation
```

---

# 📁 Repository Structure

```text
.
├── intersection/
│   ├── *.sumocfg              # SUMO configuration
│   ├── *.net.xml              # SUMO road network
│   └── ...
│
├── agent.py                   # DQN agent and action selection
├── constants.py               # Environment constants and phase mapping
├── env.py                     # SUMO/TraCI environment wrapper
├── episode.py                 # Episode execution and reward calculation
├── generator.py               # Dynamic route generation
├── main.py                    # Training entry point
├── memory.py                  # Experience Replay implementation
├── model.py                   # PyTorch MLP architecture
├── settings.py                # YAML configuration loader
├── test.py                    # Model evaluation
│
├── training_settings.yaml     # Training configuration
├── testing_settings.yaml      # Testing configuration
│
├── trained_model.pt           # Trained model weights
├── .gitignore
└── README.md
```

---

# ⚙️ Requirements

## Software

* Python **3.8+**
* SUMO Simulation Suite
* PyTorch
* NumPy
* PyYAML
* TraCI
* SUMOlib

Make sure the `SUMO_HOME` environment variable is configured correctly.

---

#  Installation

### 1. Clone the repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Install Python dependencies

```bash
pip install torch numpy pyyaml traci sumolib
```

### 3. Verify SUMO

Make sure SUMO is installed and available through the configured `SUMO_HOME` environment variable.

You can verify the installation by running:

```bash
sumo --version
```

---

#  Training

Training parameters are configured in:

```text
training_settings.yaml
```

Start training with:

```bash
python main.py
```

During training, the agent interacts with SUMO across multiple episodes and gradually learns a traffic-light control policy.

The trained model is saved as:

```text
trained_model.pt
```

---

# 🧪 Testing & Evaluation

After training, the saved model can be evaluated using:

```bash
python test.py
```

The testing configuration is controlled through:

```text
testing_settings.yaml
```

SUMO GUI can be enabled to visually observe the learned traffic-light behavior.

---

# ⚙️ Configuration

Important configuration parameters include:

| Parameter         | Description                             |
| ----------------- | --------------------------------------- |
| `gui`             | Enables or disables SUMO GUI            |
| `total_episodes`  | Number of training episodes             |
| `max_steps`       | Maximum simulation duration per episode |
| `green_duration`  | Duration of the selected green phase    |
| `yellow_duration` | Yellow-light transition duration        |
| `gamma`           | Discount factor for future rewards      |

The current discount factor is:

```text
γ = 0.95
```

---

# 📊 Evaluation Metrics

The system can be evaluated using traffic-performance indicators such as:

* Total waiting time
* Average waiting time
* Queue length
* Episode reward
* Traffic throughput
* Travel time

These metrics can be used to compare the learned DQN controller with a baseline traffic-light strategy.

---

# 🔬 Project Workflow

```text
Generate Traffic Routes
          │
          ▼
      Start SUMO
          │
          ▼
    Observe Traffic
          │
          ▼
     Extract State
          │
          ▼
      DQN Agent
          │
          ▼
     Select Action
          │
          ▼
  Change Traffic Phase
          │
          ▼
     Calculate Reward
          │
          ▼
    Store Experience
          │
          ▼
    Train DQN Model
          │
          ▼
      Next State
          │
          └───────────────► Repeat
```

---

# 📈 Expected Outcome

The expected outcome is a traffic signal controller capable of learning adaptive signal policies from simulated traffic conditions.

Instead of following a completely fixed signal schedule, the DQN agent learns to select signal phases according to the observed traffic state.

The goal is to achieve:

* Reduced vehicle waiting time
* Shorter traffic queues
* Improved traffic flow
* Better intersection efficiency
* Adaptive traffic signal control

---

# 🛠️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Main programming language |
| PyTorch    | Deep Learning / DQN       |
| SUMO       | Traffic simulation        |
| TraCI      | Python-SUMO communication |
| NumPy      | Numerical computation     |
| PyYAML     | Configuration management  |

---

# 📌 Notes

This project is designed as a **simulation-based research/academic project**. Results depend on the SUMO network configuration, generated traffic demand, training parameters, and reward design.

The trained model included in the repository can be used for evaluation without retraining, provided that the required environment and network configuration are available.

---

# 👥 Project

**Smart Traffic Light Control using Deep Q-Learning (DQN) & SUMO**

Developed as a reinforcement-learning approach for adaptive traffic signal control in simulated urban intersections, with Sofyan Tarawneh .

