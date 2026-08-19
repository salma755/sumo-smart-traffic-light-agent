# sumo-smart-traffic-light-agent
Machine learning agent trained in SUMO to optimize traffic light control and reduce congestion.


https://github.com/user-attachments/assets/c242069e-c2da-4286-8dae-d6fa486cd0b8


Smart Traffic Light Control using Deep Q-Learning (DQN) & SUMO
An AI-driven traffic management system that optimizes signal control at urban intersections using Deep Q-Networks (DQN) built with PyTorch and integrated with the SUMO (Simulation of Urban MObility) traffic simulator via TraCI.

Repository Structure

Plaintext
.
├── intersection/                 # SUMO network configuration files (.sumocfg, .net.xml)
├── agent.py                      # DQN Agent implementation & action selection logic
├── constants.py                  # Environment constants, phase maps, and spatial grid definitions
├── env.py                        # SUMO simulation wrapper using TraCI API
├── episode.py                    # Episode execution loop and wait-time/reward computation
├── generator.py                  # Dynamic route file generator (episode_routes.rou.xml)
├── main.py                       # Main entry point for training the model
├── memory.py                     # Replay memory buffer implementation (Experience Replay)
├── model.py                      # Multi-Layer Perceptron (MLP) architecture in PyTorch
├── settings.py                   # YAML settings loader utility
├── test.py                       # Evaluation script to benchmark trained models
├── testing_settings.yaml         # Configuration file for testing hyperparameters
├── training_settings.yaml        # Configuration file for training hyperparameters
├── trained_model.pt              # Saved PyTorch trained model weights
└── README.md                     # Project documentation
System Architecture & Methodology

The agent learns an optimal policy to reduce overall vehicle delay and queue formation through reinforcement learning principles:

State Representation (
S 
t
​
 
): An 
80
-element vector representing discretized spatial cells across lane groups. It captures both moving and stationary vehicles based on speed thresholds.

Action Space (
A 
t
​
 
): 
4
 discrete actions mapping to primary green phases for North-South and East-West traffic flows (including dedicated left-turn phases).

Reward Function (
R 
t
​
 
): Penalizes traffic congestion by combining cumulative waiting times and queue lengths:

R=−(waiting_time+15.0×queue_length)
Learning Mechanism: Employs Experience Replay and 
ϵ
-greedy exploration decay to stabilize Q-value approximation using a PyTorch MLP.

Getting Started

1. Prerequisites

Python 3.8+

SUMO Simulation Suite (Ensure SUMO_HOME environment variable is configured)

2. Installation

Bash
git clone <repository_url>
cd <repository_directory>
pip install torch numpy pyyaml traci sumolib
Usage

Training the Agent
To execute the full training pipeline using parameters from training_settings.yaml:

Bash
python main.py
Testing & Evaluation
To run an evaluation session using the saved model (trained_model.pt) in SUMO GUI mode:

Bash
python test.py
Configuration Parameters

Key hyperparameters can be adjusted in training_settings.yaml and testing_settings.yaml:

gui: Enable/disable SUMO graphical user interface (true/false).

total_episodes: Total number of simulation training runs.

max_steps: Total simulation duration per episode (in seconds).

green_duration: Active duration for selected green phase (in seconds).

yellow_duration: Transition duration for yellow light safety intervals.

gamma: Discount factor for future rewards (
γ=0.95
).
## Challenges

One of the main challenges we encountered was that the agent could detect the presence of congestion in specific directions, but initially struggled to understand its severity.

In other words, the agent had visibility of traffic conditions but lacked sufficient awareness of congestion magnitude. This often resulted in suboptimal traffic light decisions.

To address this issue, we refined the state representation and training process so the agent could better distinguish between different congestion levels and make more informed decisions.

## Technologies

- Python
- SUMO Simulator
- Machine Learning
- Traffic Simulation

## Learning Outcomes

Through this project, I gained practical experience in:

- Agent training
- Traffic simulation
- Feature representation
- Machine learning experimentation
- Team-based software development

  This project was developed collaboratively with Sofyan Al-Tarawneh
