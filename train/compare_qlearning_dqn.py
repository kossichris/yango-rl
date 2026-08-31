#!/usr/bin/env python3
"""Compare Q-Learning vs DQN agents."""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from env import CityEnv
from agents.qlearning import QLearnAgent
from agents.dqn import DQNAgent


def evaluate_agent(agent, env, name: str, episodes: int = 50):
    """Evaluate agent (Q-Learning or DQN).

    Args:
        agent: QLearnAgent or DQNAgent
        env: CityEnv
        name: Agent name (for printing)
        episodes: Number of evaluation episodes

    Returns:
        Dictionary with metrics
    """
    rewards = []
    trips = []

    for episode in range(episodes):
        state, _ = env.reset()
        episode_reward = 0.0
        episode_trips = 0

        for step in range(env.max_steps):
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
        "name": name,
        "avg_reward": np.mean(rewards),
        "std_reward": np.std(rewards),
        "avg_trips": np.mean(trips),
        "std_trips": np.std(trips),
    }


if __name__ == "__main__":
    print("=== Q-Learning vs DQN Comparison ===\n")

    # Create environment
    env = CityEnv(grid_size=5, demand_probability=0.5, max_steps=1000, seed=42)

    # Train Q-Learning
    print("Training Q-Learning (500 episodes)...")
    qlearn_agent = QLearnAgent(num_actions=env.num_zones)
    qlearn_metrics = qlearn_agent.train(env, episodes=500, verbose=False)

    # Train DQN
    print("Training DQN (500 episodes)...")
    dqn_agent = DQNAgent(num_actions=env.num_zones)
    dqn_metrics = dqn_agent.train(env, episodes=500, verbose=False)

    print("\n=== Training Results ===\n")

    # Evaluate both agents
    print("Evaluating Q-Learning...")
    qlearn_eval = evaluate_agent(qlearn_agent, env, "Q-Learning", episodes=50)

    print("Evaluating DQN...")
    dqn_eval = evaluate_agent(dqn_agent, env, "DQN", episodes=50)

    print("\n=== Final Metrics ===\n")

    print("Q-Learning:")
    print(f"  Reward: {qlearn_eval['avg_reward']:.0f} (±{qlearn_eval['std_reward']:.0f})")
    print(f"  Trips:  {qlearn_eval['avg_trips']:.1f} (±{qlearn_eval['std_trips']:.1f})")

    print("\nDQN:")
    print(f"  Reward: {dqn_eval['avg_reward']:.0f} (±{dqn_eval['std_reward']:.0f})")
    print(f"  Trips:  {dqn_eval['avg_trips']:.1f} (±{dqn_eval['std_trips']:.1f})")

    # Compare
    reward_diff = (dqn_eval['avg_reward'] - qlearn_eval['avg_reward']) / qlearn_eval['avg_reward'] * 100
    trips_diff = (dqn_eval['avg_trips'] - qlearn_eval['avg_trips']) / qlearn_eval['avg_trips'] * 100

    print(f"\nDQN vs Q-Learning:")
    print(f"  Reward: {reward_diff:+.1f}%")
    print(f"  Trips:  {trips_diff:+.1f}%")

    # Plot comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Training curves comparison
    ax = axes[0]
    window = 50
    qlearn_moving = np.convolve(qlearn_metrics["episode_rewards"], np.ones(window) / window, mode="valid")
    dqn_moving = np.convolve(dqn_metrics["episode_rewards"], np.ones(window) / window, mode="valid")

    ax.plot(range(window - 1, len(qlearn_metrics["episode_rewards"])), qlearn_moving, label="Q-Learning", linewidth=2)
    ax.plot(range(window - 1, len(dqn_metrics["episode_rewards"])), dqn_moving, label="DQN", linewidth=2)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.set_title("Training: Reward Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Evaluation comparison
    ax = axes[1]
    agents = ["Q-Learning", "DQN"]
    rewards = [qlearn_eval['avg_reward'], dqn_eval['avg_reward']]
    stds = [qlearn_eval['std_reward'], dqn_eval['std_reward']]

    bars = ax.bar(agents, rewards, yerr=stds, capsize=10, alpha=0.7, color=['blue', 'orange'])
    ax.set_ylabel("Avg Reward")
    ax.set_title("Evaluation: Final Performance")
    ax.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for i, (bar, reward) in enumerate(zip(bars, rewards)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height, f'{reward:.0f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("comparison_qlearning_dqn.png", dpi=100)
    print("\nComparison plot saved to: comparison_qlearning_dqn.png")
    plt.show()
