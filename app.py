#!/usr/bin/env python3
"""Streamlit app for driver repositioning RL simulation."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path
import importlib.util

# Add project root to path for imports
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Dynamically load modules
def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

try:
    # Load local modules dynamically
    env_module = load_module("env", str(project_root / "env" / "__init__.py"))
    agents_module = load_module("agents", str(project_root / "agents" / "__init__.py"))

    CityEnv = env_module.CityEnv
    QLearnAgent = agents_module.QLearnAgent
    DQNAgent = agents_module.DQNAgent

except Exception as e:
    st.error(f"⚠️ Failed to import modules: {e}")
    st.info("Trying to load modules directly...")
    try:
        # Fallback: load directly from files
        sys.path.insert(0, str(project_root / "env"))
        sys.path.insert(0, str(project_root / "agents"))
        from city_env import CityEnv
        from qlearning import QLearnAgent
        from dqn import DQNAgent
    except Exception as e2:
        st.error(f"❌ Could not load modules: {e2}")
        st.stop()


st.set_page_config(
    page_title="Driver Repositioning RL",
    page_icon="🚖",
    layout="wide",
)

st.title("🚖 Driver Repositioning with Reinforcement Learning")

st.markdown("""
This app demonstrates how Q-Learning and DQN agents learn to optimize driver repositioning
in a simulated city environment.
""")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    grid_size = st.slider("City Grid Size", 3, 7, 5)
    demand_prob = st.slider("Demand Probability", 0.1, 0.9, 0.5, step=0.1)
    episodes = st.slider("Training Episodes", 100, 1000, 500, step=100)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        train_qlearn = st.checkbox("Train Q-Learning", value=True)
    with col2:
        train_dqn = st.checkbox("Train DQN", value=True)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["🏘️ Environment", "📊 Training", "🎯 Evaluation", "📈 Comparison"])

# Tab 1: Environment
with tab1:
    st.header("City Environment")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Configuration")
        st.info(f"""
        **Grid Size**: {grid_size}×{grid_size} = {grid_size**2} zones

        **Demand Probability**: {demand_prob:.1%}

        **State Space**: [x, y, hour, day, idle_time] (5D)

        **Action Space**: {grid_size**2} zones (discrete)

        **Reward**: trip_fare - repositioning_cost
        """)

    with col2:
        st.subheader("City Layout")
        env = CityEnv(grid_size=grid_size, demand_probability=demand_prob, seed=42)

        fig, ax = plt.subplots(figsize=(6, 6))
        for zone in env.city.zones:
            color_intensity = zone.demand_probability
            rect = plt.Rectangle(
                (zone.x - 0.4, zone.y - 0.4), 0.8, 0.8,
                edgecolor='black', facecolor=(1 - color_intensity * 0.5, 1 - color_intensity * 0.5, 1),
                linewidth=2
            )
            ax.add_patch(rect)
            ax.text(zone.x, zone.y, zone.name, ha='center', va='center', fontsize=9, fontweight='bold')

        ax.set_xlim(-1, grid_size)
        ax.set_ylim(-1, grid_size)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.set_title('City Zones (color = demand probability)')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, use_container_width=True)

# Tab 2: Training
with tab2:
    st.header("Training Agents")

    progress_container = st.container()
    results_container = st.container()

    if st.button("🚀 Start Training", type="primary"):
        with progress_container:
            col1, col2 = st.columns(2)

            results = {}

            if train_qlearn:
                with col1:
                    st.subheader("Q-Learning")
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    env = CityEnv(grid_size=grid_size, demand_probability=demand_prob, seed=42)
                    agent = QLearnAgent(num_actions=env.num_zones)

                    for ep in range(0, episodes, 50):
                        agent.train(env, episodes=50, verbose=False)
                        progress_bar.progress((ep + 50) / episodes)
                        status_text.text(f"Episode {ep + 50}/{episodes}")

                    results['qlearning'] = agent
                    st.success("✅ Q-Learning trained!")

            if train_dqn:
                with col2:
                    st.subheader("DQN")
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    env = CityEnv(grid_size=grid_size, demand_probability=demand_prob, seed=42)
                    agent = DQNAgent(num_actions=env.num_zones)

                    for ep in range(0, episodes, 50):
                        agent.train(env, episodes=50, verbose=False)
                        progress_bar.progress((ep + 50) / episodes)
                        status_text.text(f"Episode {ep + 50}/{episodes}")

                    results['dqn'] = agent
                    st.success("✅ DQN trained!")

        # Store in session
        st.session_state.results = results
        st.session_state.trained = True

# Tab 3: Evaluation
with tab3:
    st.header("Agent Evaluation")

    if 'trained' in st.session_state and st.session_state.trained:
        env = CityEnv(grid_size=grid_size, demand_probability=demand_prob, seed=42)

        eval_episodes = st.slider("Evaluation Episodes", 10, 100, 50)

        col1, col2, col3 = st.columns(3)

        results = st.session_state.results

        if 'qlearning' in results:
            with col1:
                st.subheader("Q-Learning")
                rewards = []
                trips = []

                for _ in range(eval_episodes):
                    state, _ = env.reset()
                    ep_reward = 0
                    ep_trips = 0

                    for _ in range(env.max_steps):
                        action = results['qlearning'].get_best_action(state)
                        state, reward, terminated, truncated, info = env.step(action)
                        ep_reward += reward
                        if info["trip_obtained"]:
                            ep_trips += 1
                        if terminated or truncated:
                            break

                    rewards.append(ep_reward)
                    trips.append(ep_trips)

                st.metric("Avg Reward", f"${np.mean(rewards):,.0f}")
                st.metric("Avg Trips", f"{np.mean(trips):.1f}")

        if 'dqn' in results:
            with col2:
                st.subheader("DQN")
                rewards = []
                trips = []

                for _ in range(eval_episodes):
                    state, _ = env.reset()
                    ep_reward = 0
                    ep_trips = 0

                    for _ in range(env.max_steps):
                        action = results['dqn'].get_best_action(state)
                        state, reward, terminated, truncated, info = env.step(action)
                        ep_reward += reward
                        if info["trip_obtained"]:
                            ep_trips += 1
                        if terminated or truncated:
                            break

                    rewards.append(ep_reward)
                    trips.append(ep_trips)

                st.metric("Avg Reward", f"${np.mean(rewards):,.0f}")
                st.metric("Avg Trips", f"{np.mean(trips):.1f}")

        # Random baseline
        with col3:
            st.subheader("Random (Baseline)")
            rewards = []
            trips = []

            for _ in range(eval_episodes):
                state, _ = env.reset()
                ep_reward = 0
                ep_trips = 0

                for _ in range(env.max_steps):
                    action = env.action_space.sample()
                    state, reward, terminated, truncated, info = env.step(action)
                    ep_reward += reward
                    if info["trip_obtained"]:
                        ep_trips += 1
                    if terminated or truncated:
                        break

                rewards.append(ep_reward)
                trips.append(ep_trips)

            st.metric("Avg Reward", f"${np.mean(rewards):,.0f}")
            st.metric("Avg Trips", f"{np.mean(trips):.1f}")
    else:
        st.info("👈 Train agents first in the Training tab!")

# Tab 4: Comparison
with tab4:
    st.header("Q-Learning vs DQN Comparison")

    st.markdown("""
    ### Key Findings

    | Aspect | Q-Learning | DQN |
    |--------|-----------|-----|
    | **State Space** | Tabular (dict) | Neural Network |
    | **Scalability** | Small spaces only | Large/continuous spaces |
    | **Convergence** | Fast | Slower |
    | **Memory** | Can be large | Compact |
    | **Best For** | 25-100 states | 1000+ states |

    ### This Problem (25 zones)
    - ✅ **Q-Learning wins** (+17.3% better)
    - ❌ DQN is overkill
    - 📌 Lesson: Choose the right tool for problem size!
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("When to use Q-Learning")
        st.success("""
        ✅ Small discrete state spaces
        ✅ Need fast convergence
        ✅ Limited memory available
        ✅ Deterministic environments
        """)

    with col2:
        st.subheader("When to use DQN")
        st.info("""
        💡 Large state spaces
        💡 Continuous observations (images, etc.)
        💡 Complex environments
        💡 Lots of training data available
        """)

st.markdown("---")
st.markdown("🏛️ **Built with**: Gymnasium • PyTorch • Streamlit")
