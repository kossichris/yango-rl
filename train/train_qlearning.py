#!/usr/bin/env python3
"""Train Q-Learning agent on CityEnv."""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from env import CityEnv
from agents.qlearning import QLearnAgent


def train_qlearning(
    episodes: int = 500,
    grid_size: int = 5,
    demand_probability: float = 0.5,
    learning_rate: float = 0.1,
    discount_factor: float = 0.99,
    epsilon: float = 0.1,
    epsilon_decay: float = 0.995,
    seed: int = 42,
):
    """Train Q-Learning agent.

    Args:
        episodes: Number of training episodes
        grid_size: City grid size
        demand_probability: Base demand probability per zone
        learning_rate: α parameter
        discount_factor: γ parameter
        epsilon: ε parameter
        epsilon_decay: Decay rate for epsilon
        seed: Random seed
    """
    print("=== Q-Learning Training ===\n")

    # Create environment
    env = CityEnv(
        grid_size=grid_size,
        demand_probability=demand_probability,
        max_steps=1000,
        seed=seed,
    )

    # Create agent
    agent = QLearnAgent(
        num_actions=env.num_zones,
        learning_rate=learning_rate,
        discount_factor=discount_factor,
        epsilon=epsilon,
        epsilon_decay=epsilon_decay,
    )

    print(f"Environment: {grid_size}x{grid_size} grid ({env.num_zones} zones)")
    print(f"Agent: α={learning_rate}, γ={discount_factor}, ε={epsilon}")
    print(f"Training: {episodes} episodes\n")

    # Train agent
    metrics = agent.train(env, episodes=episodes, verbose=True)

    print("\n=== Training Complete ===\n")

    # Extract metrics
    episode_rewards = metrics["episode_rewards"]
    episode_trips = metrics["episode_trips"]

    # Calculate statistics
    last_50_rewards = episode_rewards[-50:]
    last_50_trips = episode_trips[-50:]

    print(f"Final 50 episodes (avg):")
    print(f"  Reward: {np.mean(last_50_rewards):.2f} (±{np.std(last_50_rewards):.2f})")
    print(f"  Trips: {np.mean(last_50_trips):.2f} (±{np.std(last_50_trips):.2f})")
    print(f"  Final ε: {agent.epsilon:.4f}")
    print(f"  Q-table size: {len(agent.Q)} states")

    # Plot results
    plot_training_results(episode_rewards, episode_trips)

    return agent, metrics


def plot_training_results(rewards: list, trips: list):
    """Plot training curves.

    Args:
        rewards: List of episode rewards
        trips: List of episode trips
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Reward plot
    ax = axes[0]
    ax.plot(rewards, alpha=0.3, label="Per episode")
    window = 50
    moving_avg = np.convolve(rewards, np.ones(window) / window, mode="valid")
    ax.plot(range(window - 1, len(rewards)), moving_avg, label=f"Moving avg (window={window})", linewidth=2)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.set_title("Episode Reward")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Trips plot
    ax = axes[1]
    ax.plot(trips, alpha=0.3, label="Per episode")
    moving_avg = np.convolve(trips, np.ones(window) / window, mode="valid")
    ax.plot(range(window - 1, len(trips)), moving_avg, label=f"Moving avg (window={window})", linewidth=2)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Trips Obtained")
    ax.set_title("Episode Trips")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("training_results.png", dpi=100)
    print("\nPlot saved to: training_results.png")
    plt.show()


if __name__ == "__main__":
    agent, metrics = train_qlearning(
        episodes=500,
        grid_size=5,
        demand_probability=0.5,
        learning_rate=0.1,
        discount_factor=0.99,
        epsilon=0.1,
        epsilon_decay=0.995,
        seed=42,
    )
