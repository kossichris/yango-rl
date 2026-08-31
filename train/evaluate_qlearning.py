#!/usr/bin/env python3
"""Evaluate Q-Learning agent performance."""

import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from env import CityEnv
from agents.qlearning import QLearnAgent


def evaluate_agent(agent, env, episodes: int = 50):
    """Evaluate agent performance.

    Args:
        agent: Trained QLearnAgent
        env: CityEnv environment
        episodes: Number of evaluation episodes

    Returns:
        Dictionary with evaluation metrics
    """
    rewards = []
    trips = []

    for episode in range(episodes):
        state, _ = env.reset()
        episode_reward = 0.0
        episode_trips = 0

        for step in range(env.max_steps):
            # Pure exploitation (no exploration)
            action = agent.get_best_action(state)
            next_state, reward, terminated, truncated, info = env.step(action)

            episode_reward += reward
            if info["trip_obtained"]:
                episode_trips += 1

            state = next_state

            if terminated or truncated:
                break

        rewards.append(episode_reward)
        trips.append(episode_trips)

    return {
        "avg_reward": np.mean(rewards),
        "std_reward": np.std(rewards),
        "avg_trips": np.mean(trips),
        "std_trips": np.std(trips),
        "rewards": rewards,
        "trips": trips,
    }


def evaluate_random_baseline(env, episodes: int = 50):
    """Evaluate random policy baseline.

    Args:
        env: CityEnv environment
        episodes: Number of evaluation episodes

    Returns:
        Dictionary with baseline metrics
    """
    rewards = []
    trips = []

    for episode in range(episodes):
        state, _ = env.reset()
        episode_reward = 0.0
        episode_trips = 0

        for step in range(env.max_steps):
            # Random action
            action = env.action_space.sample()
            next_state, reward, terminated, truncated, info = env.step(action)

            episode_reward += reward
            if info["trip_obtained"]:
                episode_trips += 1

            state = next_state

            if terminated or truncated:
                break

        rewards.append(episode_reward)
        trips.append(episode_trips)

    return {
        "avg_reward": np.mean(rewards),
        "std_reward": np.std(rewards),
        "avg_trips": np.mean(trips),
        "std_trips": np.std(trips),
        "rewards": rewards,
        "trips": trips,
    }


def analyze_learned_policy(agent, env):
    """Analyze learned policy by checking Q-values.

    Args:
        agent: Trained QLearnAgent
        env: CityEnv environment
    """
    print("\n=== Learned Policy Analysis ===\n")

    # Find top Q-states
    top_states = sorted(
        agent.Q.items(),
        key=lambda x: np.max(x[1]),
        reverse=True
    )[:10]

    print("Top 10 best states (by max Q-value):\n")
    for i, (state_key, q_values) in enumerate(top_states, 1):
        x, y, hour, day, idle = state_key
        best_action = np.argmax(q_values)
        best_q = np.max(q_values)
        zone_name = env.city.get_zone(best_action).name
        day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][day]

        print(f"{i}. State: ({x:.1f}, {y:.1f}) at {int(hour):02d}h {day_name} (idle={int(idle)}s)")
        print(f"   → Best action: Zone {zone_name} (Q={best_q:.0f})")
        print()

    # Average Q-value statistics
    all_q_values = []
    for q_vals in agent.Q.values():
        all_q_values.extend(q_vals)

    print(f"\nQ-Table Statistics:")
    print(f"  Total states: {len(agent.Q)}")
    print(f"  Total state-action pairs: {len(all_q_values)}")
    print(f"  Avg Q-value: {np.mean(all_q_values):.0f}")
    print(f"  Max Q-value: {np.max(all_q_values):.0f}")
    print(f"  Min Q-value: {np.min(all_q_values):.0f}")


if __name__ == "__main__":
    print("=== Q-Learning Agent Evaluation ===\n")

    # Create environment
    env = CityEnv(grid_size=5, demand_probability=0.5, max_steps=1000, seed=42)

    # Create and train agent
    agent = QLearnAgent(num_actions=env.num_zones)
    print("Training agent (500 episodes)...")
    metrics = agent.train(env, episodes=500, verbose=False)

    print("\n=== Evaluation Results ===\n")

    # Evaluate trained agent
    print("Evaluating trained Q-Learning agent...")
    trained_metrics = evaluate_agent(agent, env, episodes=50)

    print(f"Q-Learning Agent:")
    print(f"  Avg reward: {trained_metrics['avg_reward']:.0f} (±{trained_metrics['std_reward']:.0f})")
    print(f"  Avg trips: {trained_metrics['avg_trips']:.1f} (±{trained_metrics['std_trips']:.1f})")

    # Evaluate random baseline
    print("\nEvaluating random baseline...")
    random_metrics = evaluate_random_baseline(env, episodes=50)

    print(f"Random Policy:")
    print(f"  Avg reward: {random_metrics['avg_reward']:.0f} (±{random_metrics['std_reward']:.0f})")
    print(f"  Avg trips: {random_metrics['avg_trips']:.1f} (±{random_metrics['std_trips']:.1f})")

    # Calculate improvement
    reward_improvement = (trained_metrics['avg_reward'] - random_metrics['avg_reward']) / abs(random_metrics['avg_reward']) * 100
    trips_improvement = (trained_metrics['avg_trips'] - random_metrics['avg_trips']) / abs(random_metrics['avg_trips']) * 100

    print(f"\nImprovement over random:")
    print(f"  Reward: {reward_improvement:+.1f}%")
    print(f"  Trips: {trips_improvement:+.1f}%")

    # Analyze learned policy
    analyze_learned_policy(agent, env)
