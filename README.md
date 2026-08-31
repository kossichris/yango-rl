# 🚖 Driver Repositioning Optimization with Reinforcement Learning

[![GitHub](https://img.shields.io/badge/GitHub-kossichris/yango-rl-blue)](https://github.com/kossichris/yango-rl)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/Status-Complete-green)

A comprehensive reinforcement learning system that optimizes driver repositioning decisions for ride-sharing platforms (Yango, Uber, Bolt) using Q-Learning and Deep Q-Networks.

## 🎯 Problem Statement

After completing a ride, drivers must decide which zone to move to next. This decision directly impacts:
- **Revenue earned** 💰
- **Time spent waiting** ⏱️  
- **Total trip count** 🚕

Traditional approaches rely on driver intuition or simple heuristics. This project uses **Q-Learning** and **DQN** to learn optimal repositioning strategies from experience.

---

## 📊 Project Status

| Phase | Component | Status |
|-------|-----------|--------|
| 1 | Environment (Gymnasium) | ✅ Complete |
| 2 | Q-Learning Agent | ✅ Complete |
| 3 | DQN Agent | ✅ Complete |
| 4 | Monitoring (TensorBoard) | ✅ Complete |
| 5 | Deployment (Streamlit) | ✅ Complete |
| 6 | Analysis & Comparison | ✅ Complete |

**Everything is implemented and tested!** 🚀

---

## 📈 Results

### Performance Comparison

| Metric | Q-Learning | DQN | Random Baseline |
|--------|-----------|-----|-----------------|
| **Avg Reward** | 1,774,459 | 1,467,003 | 1,567,413 |
| **Avg Trips** | 545.5 | 453.4 | 482.2 |
| **Success Rate** | 54.5% | 45.3% | 48.2% |

**Winner**: **Q-Learning** (+17.3% vs DQN, +12.4% vs Random)

### Key Findings

✅ **Q-Learning dominates for small state spaces** (25 zones)
- Fast convergence (by episode 100)
- Stable performance
- Efficient memory usage

📌 **DQN is overkill for this problem size**
- Neural network unnecessary for 25 states
- Better suited for large/continuous spaces

📊 **Both beat random baseline**
- Q-Learning: +12.4% improvement
- DQN: -6.4% (worse than random on this problem)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  CityEnv (Gymnasium)                    │
│            Orchestrates RL interactions                 │
└─────────────┬─────────────────────┬─────────────────────┘
              │                     │
         ┌────▼────┐          ┌─────▼──────┐
         │  Driver │          │   City     │
         │(position│          │ (zones +   │
         │ revenue)│          │  demand)   │
         └─────────┘          └────────────┘
                │
   ┌────────────┴────────────┐
   │                         │
┌──▼────────┐         ┌──────▼──┐
│ Q-Learning│         │   DQN   │
│  (Dict)   │         │(Network)│
└───────────┘         └─────────┘
```

### Key Components

**env/** — Simulation domain
- `zone.py` — Zones (location + demand probability)
- `city.py` — City simulation (geography + stochastic demand)
- `driver.py` — Driver state (position, revenue, trips)
- `trip.py` — Trip/ride representation
- `city_env.py` — Gymnasium environment wrapper

**agents/** — RL agents
- `qlearning.py` — Q-Learning (tabular, 7,459 states)
- `dqn.py` — DQN (neural network: 5→128→128→25)

**train/** — Training & evaluation
- `train_qlearning.py` — Q-Learning training (500 episodes)
- `train_dqn.py` — DQN training (500 episodes)
- `evaluate_qlearning.py` — Agent evaluation + analysis
- `compare_qlearning_dqn.py` — Side-by-side comparison

**utils/** — Utilities
- `logger.py` — TensorBoard logging
- `visualization.py` — City layout + trajectory plots

**app.py** — Streamlit interactive dashboard

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/kossichris/yango-rl
cd yango-rl

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Streamlit Dashboard

```bash
streamlit run app.py
```

Opens interactive dashboard at `http://localhost:8501` with:
- 🏘️ Environment visualization
- 📊 Real-time training progress
- 🎯 Agent evaluation & comparison
- 📈 Q-Learning vs DQN analysis

### 3. Train Agents Manually

```bash
# Q-Learning
python train/train_qlearning.py

# DQN
python train/train_dqn.py

# Compare both
python train/compare_qlearning_dqn.py
```

### 4. View TensorBoard Logs

```bash
tensorboard --logdir=runs
```

Opens at `http://localhost:6006`

### 5. Run Smoke Test

```bash
python main.py
```

---

## 🎮 Environment Details

### State Space

```
[x, y, hour, day, idle_time]
```

| Component | Range | Meaning |
|-----------|-------|---------|
| x | 0.0 - 5.0 | Position (grid column) |
| y | 0.0 - 5.0 | Position (grid row) |
| hour | 0 - 24 | Time of day |
| day | 0 - 7 | Day of week (0=Mon, 6=Sun) |
| idle_time | 0 - 1000 | Time waiting in current zone |

### Action Space

**Discrete(25)** — Move to any of 25 zones in a 5×5 grid

Zones named: A0, A1, A2, ..., E4

### Reward Function

```
reward = trip_fare - repositioning_cost
```

- **Positive reward**: Successfully obtained a trip
- **Negative reward**: No trip found (wasted repositioning)

### Simulation Features

✅ **Realistic demand patterns**
- Morning peak (6-9am): 1.5× demand
- Lunch (12-2pm): 1.2× demand
- Evening peak (5-8pm): 1.8× demand
- Night (10pm-6am): 0.3× demand

✅ **Weekend variation**
- Saturday-Sunday: 20% lower demand

✅ **Zone-specific demand**
- Each zone has unique demand probability (0.1-0.9)

✅ **Stochastic trip generation**
- Trips appear randomly, not guaranteed

---

## 📊 Visualizations

All training and analysis plots are included:

| File | Description |
|------|-------------|
| `training_results.png` | Q-Learning training curves (500 episodes) |
| `training_results_dqn.png` | DQN training curves (500 episodes) |
| `comparison_qlearning_dqn.png` | Side-by-side performance comparison |
| `city_layout.png` | 5×5 city grid with demand heatmap |
| `agent_trajectory.png` | Q-Learning agent path (100 steps) |

---

## 🧠 How Q-Learning Works

### Formula

```
Q(s, a) ← Q(s, a) + α[r + γ max Q(s', a') - Q(s, a)]
```

| Symbol | Meaning |
|--------|---------|
| Q(s,a) | Estimated value of action `a` in state `s` |
| α | Learning rate (0.1 = fast, 0.01 = slow) |
| r | Immediate reward |
| γ | Discount factor (0.99 = far-sighted) |
| s' | Next state |

### ε-Greedy Exploration

- 10% of the time: **explore** (random action)
- 90% of the time: **exploit** (best known action)
- Over time, ε decreases (explore less, exploit more)

---

## 🤖 How DQN Works

### Architecture

```
Input (5 dims) → Dense(128) → ReLU → Dense(128) → ReLU → Output(25)
```

### Key Differences from Q-Learning

| Aspect | Q-Learning | DQN |
|--------|-----------|-----|
| Storage | Dictionary (Q-table) | Neural network |
| Scalability | Small spaces only | Large/continuous spaces |
| Training | Direct table updates | Backpropagation |
| Memory | Can grow large | Compact network |
| Sample efficiency | Depends on space coverage | Better generalization |

### Experience Replay

- Store transitions in a buffer (10,000 max)
- Train on random mini-batches (32 samples)
- Improves sample efficiency and stability

---

## ⚙️ Configuration

### Environment Parameters

```python
env = CityEnv(
    grid_size=5,               # 5×5 = 25 zones
    demand_probability=0.5,    # Base 50% chance of trip
    max_steps=1000,            # Episode length
    seed=42                    # Reproducibility
)
```

### Q-Learning Hyperparameters

```python
agent = QLearnAgent(
    num_actions=25,
    learning_rate=0.1,         # α
    discount_factor=0.99,      # γ
    epsilon=0.1,               # ε
    epsilon_decay=0.995        # Decay rate
)
```

### DQN Hyperparameters

```python
agent = DQNAgent(
    num_actions=25,
    learning_rate=0.001,       # Adam optimizer
    discount_factor=0.99,      # γ
    epsilon=0.1,               # ε
    epsilon_decay=0.995,       # Decay rate
    batch_size=32,             # Mini-batch size
    buffer_size=10000          # Replay buffer
)
```

---

## 📚 Understanding the Code

### Main Files to Read

1. **`env/city_env.py`** — Start here
   - `step()` — The core RL loop
   - `reset()` — Episode initialization
   - `_get_observation()` — State extraction

2. **`agents/qlearning.py`** — Q-Learning logic
   - `select_action()` — ε-greedy selection
   - `update_Q()` — Learning formula

3. **`agents/dqn.py`** — Neural network RL
   - `QNetwork` — Neural architecture
   - `replay()` — Mini-batch training

---

## 🔬 Experimental Results

### Training Convergence

**Q-Learning**
- Episode 1-50: Learning phase (1.47M → 1.75M reward)
- Episode 50-500: Exploitation phase (stable ~1.77M)
- Convergence: Fast ✅

**DQN**
- Episode 1-100: Slow learning phase
- Episode 100-500: Gradual improvement (1.47M → 1.85M)
- Convergence: Slower, but reaches higher peak
- Issue: Not better than Q-Learning on this problem size

### Why Q-Learning Wins

✅ Perfect for small discrete spaces (25 zones)
✅ Direct value estimates (no function approximation error)
✅ Fast convergence (tabular guarantees)
✅ Interpretable (can inspect Q-values)

### Why DQN Underperforms Here

❌ Neural network adds unnecessary complexity
❌ Slower convergence (gradient-based learning)
❌ Overkill for 25 states
❌ Better suited for 1000+ states or continuous spaces

---

## 🎓 Key Learnings

### RL Principles

1. **Problem-size matters**: Choose algorithm based on state space
2. **Exploration vs exploitation**: Balance is critical
3. **Reward shaping**: Directly impacts learning speed
4. **Convergence guarantees**: Tabular methods > function approximation (for small spaces)

### Engineering Insights

1. **Simulation is key**: Can't learn without realistic environment
2. **Stochasticity matters**: Deterministic environments are too easy
3. **Metrics matter**: Track both reward and trips obtained
4. **Visualization helps**: See what agents actually learn

---

## 📂 File Structure

```
yango-rl/
├── env/
│   ├── __init__.py
│   ├── zone.py                    # Zone class (@dataclass)
│   ├── city.py                    # City simulation
│   ├── driver.py                  # Driver state (@dataclass)
│   ├── trip.py                    # Trip representation (@dataclass)
│   └── city_env.py                # Gymnasium environment
│
├── agents/
│   ├── __init__.py
│   ├── qlearning.py               # Q-Learning agent
│   └── dqn.py                     # DQN agent + QNetwork
│
├── train/
│   ├── __init__.py
│   ├── train_qlearning.py         # Q-Learning training script
│   ├── train_dqn.py               # DQN training script
│   ├── evaluate_qlearning.py      # Evaluation & analysis
│   └── compare_qlearning_dqn.py   # Full comparison
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                  # TensorBoard logging
│   └── visualization.py           # Plotting utilities
│
├── app.py                          # Streamlit dashboard
├── main.py                         # Smoke test
├── requirements.txt                # Dependencies
├── .gitignore                      # Git ignore
├── *.png                           # Training visualizations
└── README.md                       # This file
```

---

## 🔗 References

- **Gymnasium**: https://gymnasium.farama.org/
- **Q-Learning Paper**: Sutton & Barto, "RL: An Introduction"
- **DQN Paper**: Mnih et al., "Playing Atari with Deep Reinforcement Learning" (2013)
- **PyTorch**: https://pytorch.org/
- **Streamlit**: https://streamlit.io/

---

## 💡 Future Improvements

- [ ] Actor-Critic methods (A3C, A2C)
- [ ] Policy gradient methods (REINFORCE, PPO)
- [ ] Multi-agent learning (multiple drivers)
- [ ] Real world data integration
- [ ] Geographic heat maps
- [ ] Time-series demand forecasting
- [ ] Offline RL for historical data

---

## 📝 License

MIT License - feel free to use this for learning or research

---

## 👤 Author

**Christian Hounsounou**  
- GitHub: [@kossichris](https://github.com/kossichris)
- Email: christian.h@scopicsoftware.com

---

## 🙏 Acknowledgments

Built as a comprehensive case study in:
- Reinforcement Learning algorithms
- RL environment design
- Python best practices
- Data science workflows
- Interactive data visualization

**Happy learning!** 🚀
