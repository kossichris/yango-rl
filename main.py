#!/usr/bin/env python3
"""Smoke test: verify the environment works correctly."""

import numpy as np
from env import CityEnv


def test_env():
    """Run a quick test of the environment."""
    print("=== CityEnv Smoke Test ===\n")

    env = CityEnv(grid_size=5, demand_probability=0.5, max_steps=50, seed=42)

    obs, info = env.reset()
    print(f"Initial observation: {obs}")
    print(f"Observation space: {env.observation_space}")
    print(f"Action space: {env.action_space}")
    print(f"Num zones: {env.num_zones}\n")

    total_reward = 0.0
    trips_obtained = 0

    for step in range(50):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

        total_reward += reward
        if info["trip_obtained"]:
            trips_obtained += 1

        if step % 10 == 0:
            print(
                f"Step {step:3d}: ({info['x']:.1f}, {info['y']:.1f}), Idle {obs[4]:.1f}, "
                f"Revenue {info['total_revenue']:7.2f}, "
                f"Trips {info['completed_trips']:3d}, Reward {reward:6.2f}"
            )

        if terminated:
            print(f"\nEpisode terminated at step {step}")
            break

    print(f"\n=== Episode Summary ===")
    print(f"Total steps: {env.current_step}")
    print(f"Total reward: {total_reward:.2f}")
    print(f"Total revenue: {env.driver.total_revenue:.2f}")
    print(f"Trips completed: {env.driver.completed_trips}")
    print(f"Trips obtained: {trips_obtained}")
    print(f"Success rate: {trips_obtained / env.current_step * 100:.1f}%")


if __name__ == "__main__":
    test_env()
