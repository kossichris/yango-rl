#!/usr/bin/env python3
"""Visualization utilities for CityEnv."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from env import CityEnv


def visualize_city(env, agent=None):
    """Visualize city zones and demand.

    Args:
        env: CityEnv environment
        agent: Optional QLearnAgent (to show best actions)
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw zones
    for zone in env.city.zones:
        color_intensity = zone.demand_probability  # Darker = higher demand
        rect = patches.Rectangle(
            (zone.x - 0.4, zone.y - 0.4),
            0.8,
            0.8,
            linewidth=2,
            edgecolor='black',
            facecolor=(1 - color_intensity * 0.5, 1 - color_intensity * 0.5, 1),
        )
        ax.add_patch(rect)

        # Add zone name and demand probability
        ax.text(zone.x, zone.y + 0.15, zone.name, ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(zone.x, zone.y - 0.15, f'{zone.demand_probability:.2f}', ha='center', va='center', fontsize=9)

    # Draw grid
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 5)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_xlabel('X Position', fontsize=12)
    ax.set_ylabel('Y Position', fontsize=12)
    ax.set_title('City Zones (color intensity = demand probability)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('city_layout.png', dpi=100)
    print("City layout saved to: city_layout.png")
    plt.show()


def simulate_and_visualize(env, agent, num_steps: int = 50):
    """Simulate agent on environment and show trajectory.

    Args:
        env: CityEnv environment
        agent: QLearnAgent (trained)
        num_steps: Number of steps to simulate
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw zones
    for zone in env.city.zones:
        color_intensity = zone.demand_probability
        rect = patches.Rectangle(
            (zone.x - 0.4, zone.y - 0.4),
            0.8,
            0.8,
            linewidth=2,
            edgecolor='black',
            facecolor=(1 - color_intensity * 0.5, 1 - color_intensity * 0.5, 1),
        )
        ax.add_patch(rect)
        ax.text(zone.x, zone.y, zone.name, ha='center', va='center', fontsize=10, fontweight='bold')

    # Simulate trajectory
    state, _ = env.reset()
    positions = [(state[0], state[1])]
    actions_taken = []
    rewards_taken = []

    for step in range(num_steps):
        action = agent.get_best_action(state)
        next_state, reward, terminated, truncated, info = env.step(action)

        positions.append((next_state[0], next_state[1]))
        actions_taken.append(action)
        rewards_taken.append(reward)

        state = next_state

        if terminated or truncated:
            break

    # Draw trajectory
    xs, ys = zip(*positions)
    ax.plot(xs, ys, 'r-', alpha=0.5, linewidth=2, label='Trajectory')
    ax.scatter(xs[0], ys[0], color='green', s=200, marker='o', label='Start', zorder=5)
    ax.scatter(xs[-1], ys[-1], color='red', s=200, marker='X', label='End', zorder=5)
    ax.scatter(xs[1:-1], ys[1:-1], color='orange', s=50, alpha=0.6, label='Visited', zorder=4)

    # Add statistics
    total_reward = sum(rewards_taken)
    trips = sum(1 for r in rewards_taken if r > 0)
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 5)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_xlabel('X Position', fontsize=12)
    ax.set_ylabel('Y Position', fontsize=12)
    ax.set_title(f'Agent Trajectory ({len(positions)} steps, {trips} trips, reward={total_reward:.0f})', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('agent_trajectory.png', dpi=100)
    print("Agent trajectory saved to: agent_trajectory.png")
    plt.show()

    print(f"\nTrajectory Summary:")
    print(f"  Steps: {len(positions)}")
    print(f"  Trips obtained: {trips}")
    print(f"  Total reward: {total_reward:.0f}")
    print(f"  Avg reward per step: {total_reward / len(positions):.0f}")


if __name__ == "__main__":
    from agents.qlearning import QLearnAgent

    print("=== City Visualization ===\n")

    # Create environment
    env = CityEnv(grid_size=5, demand_probability=0.5, seed=42)

    # Visualize city
    print("Generating city layout...")
    visualize_city(env)

    # Train agent
    print("\nTraining agent...")
    agent = QLearnAgent(num_actions=env.num_zones)
    agent.train(env, episodes=500, verbose=False)

    # Visualize trajectory
    print("Generating agent trajectory...")
    simulate_and_visualize(env, agent, num_steps=100)
