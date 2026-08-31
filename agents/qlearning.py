import numpy as np
import random
from typing import Tuple, Optional, Dict, List


class QLearnAgent:
    """Q-Learning agent for driver repositioning optimization."""

    def __init__(
        self,
        num_actions: int,
        learning_rate: float = 0.1,
        discount_factor: float = 0.99,
        epsilon: float = 0.1,
        epsilon_decay: float = 0.995,
    ):
        """Initialize Q-Learning agent.

        Args:
            num_actions: Number of possible actions (zones)
            learning_rate: α - how fast to learn (0.1 = fast, 0.01 = slow)
            discount_factor: γ - weight of future rewards (0.99 = far-sighted)
            epsilon: ε - exploration rate (0.1 = 10% random, 90% best)
            epsilon_decay: decay rate for epsilon (0.995 = slowly decrease exploration)
        """
        self.num_actions = num_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = 0.01

        self.Q = {}  # Q-table: state → [Q_0, Q_1, ..., Q_n]
        self.episode_rewards = []  # Track rewards per episode
        self.episode_trips = []  # Track trips obtained per episode

    def _state_to_key(self, state: np.ndarray) -> Tuple:
        """Convert observation array to hashable tuple for Q-table.

        Args:
            state: [x, y, hour, day, idle_time]

        Returns:
            Rounded tuple for Q-table key
        """
        x, y, hour, day, idle_time = state
        return (round(x, 1), round(y, 1), int(hour), int(day), int(idle_time))

    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Select action using ε-greedy strategy.

        Args:
            state: Current observation [x, y, hour, day, idle_time]
            training: If True, use exploration; if False, pure exploitation

        Returns:
            Action (zone_id 0-24)
        """
        state_key = self._state_to_key(state)

        # If state not seen before, initialize Q-values to 0
        if state_key not in self.Q:
            self.Q[state_key] = np.zeros(self.num_actions)

        # ε-greedy: random action with prob ε, best action with prob 1-ε
        if training and random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)  # Explore: random
        else:
            return int(np.argmax(self.Q[state_key]))  # Exploit: best Q-value

    def update_Q(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        """Update Q-table using Q-Learning formula.

        Args:
            state: Current state [x, y, hour, day, idle_time]
            action: Action taken (zone_id)
            reward: Reward received
            next_state: Next state [x, y, hour, day, idle_time]
            done: Whether episode is finished
        """
        state_key = self._state_to_key(state)
        next_state_key = self._state_to_key(next_state)

        # Initialize Q-values if state not seen before
        if state_key not in self.Q:
            self.Q[state_key] = np.zeros(self.num_actions)
        if next_state_key not in self.Q:
            self.Q[next_state_key] = np.zeros(self.num_actions)

        # Q-Learning formula: Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
        current_Q = self.Q[state_key][action]
        max_next_Q = np.max(self.Q[next_state_key]) if not done else 0
        new_Q = current_Q + self.lr * (reward + self.gamma * max_next_Q - current_Q)
        self.Q[state_key][action] = new_Q

    def decay_epsilon(self) -> None:
        """Decrease exploration rate (explore less, exploit more over time)."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def train(self, env, episodes: int = 500, verbose: bool = True) -> Dict:
        """Train agent on environment.

        Args:
            env: Gymnasium environment (CityEnv)
            episodes: Number of episodes to train
            verbose: Print progress every 50 episodes

        Returns:
            Dictionary with training metrics
        """
        for episode in range(episodes):
            state, _ = env.reset()
            episode_reward = 0.0
            episode_trips = 0

            for step in range(env.max_steps):
                # Select action (ε-greedy)
                action = self.select_action(state, training=True)

                # Take action in environment
                next_state, reward, terminated, truncated, info = env.step(action)

                # Update Q-table
                done = terminated or truncated
                self.update_Q(state, action, reward, next_state, done)

                episode_reward += reward
                if info["trip_obtained"]:
                    episode_trips += 1

                state = next_state

                if done:
                    break

            # Decay exploration rate
            self.decay_epsilon()

            # Track metrics
            self.episode_rewards.append(episode_reward)
            self.episode_trips.append(episode_trips)

            # Print progress
            if verbose and (episode + 1) % 50 == 0:
                avg_reward = np.mean(self.episode_rewards[-50:])
                avg_trips = np.mean(self.episode_trips[-50:])
                print(f"Episode {episode + 1}/{episodes} | Avg Reward: {avg_reward:.2f} | Avg Trips: {avg_trips:.1f} | ε: {self.epsilon:.3f}")

        return {
            "episode_rewards": self.episode_rewards,
            "episode_trips": self.episode_trips,
            "Q_table": self.Q,
        }

    def get_best_action(self, state: np.ndarray) -> int:
        """Get best action without exploration (pure exploitation).

        Args:
            state: Current observation

        Returns:
            Best action (zone_id)
        """
        return self.select_action(state, training=False)
