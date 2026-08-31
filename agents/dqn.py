import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from typing import Tuple, Dict, List
from collections import deque


class QNetwork(nn.Module):
    """Neural network for Q-value prediction."""

    def __init__(self, state_size: int = 5, action_size: int = 25, hidden_size: int = 128):
        """Initialize network.

        Args:
            state_size: Dimension of state (5: x, y, hour, day, idle_time)
            action_size: Number of actions (25 zones)
            hidden_size: Hidden layer size
        """
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)
        self.relu = nn.ReLU()

    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """Forward pass: State → Q-values.

        Args:
            state: Observation tensor [batch_size, 5]

        Returns:
            Q-values [batch_size, 25]
        """
        x = self.relu(self.fc1(state))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class DQNAgent:
    """Deep Q-Network agent."""

    def __init__(
        self,
        num_actions: int = 25,
        state_size: int = 5,
        learning_rate: float = 0.001,
        discount_factor: float = 0.99,
        epsilon: float = 0.1,
        epsilon_decay: float = 0.995,
        batch_size: int = 32,
        buffer_size: int = 10000,
    ):
        """Initialize DQN agent.

        Args:
            num_actions: Number of actions (25 zones)
            state_size: State dimension (5)
            learning_rate: Learning rate for optimizer
            discount_factor: γ - discount future rewards
            epsilon: ε - exploration rate
            epsilon_decay: Decay factor for epsilon
            batch_size: Mini-batch size for training
            buffer_size: Replay buffer size
        """
        self.num_actions = num_actions
        self.state_size = state_size
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = 0.01
        self.batch_size = batch_size

        # Network
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.network = QNetwork(state_size, num_actions).to(self.device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()

        # Replay buffer
        self.memory = deque(maxlen=buffer_size)

        # Training metrics
        self.episode_rewards = []
        self.episode_trips = []

    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Select action using ε-greedy.

        Args:
            state: Current observation [x, y, hour, day, idle_time]
            training: Whether in training mode (use exploration)

        Returns:
            Action (zone_id 0-24)
        """
        # ε-greedy: explore with prob ε, exploit with prob 1-ε
        if training and random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)

        # Exploit: use network to predict best action
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.network(state_tensor)
        return int(q_values.argmax(dim=1).item())

    def remember(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool) -> None:
        """Store experience in replay buffer.

        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode finished
        """
        self.memory.append((state, action, reward, next_state, done))

    def replay(self) -> float:
        """Train network on mini-batch from replay buffer.

        Returns:
            Loss value
        """
        if len(self.memory) < self.batch_size:
            return 0.0

        # Sample mini-batch
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convert to tensors
        states_tensor = torch.FloatTensor(np.array(states)).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_states_tensor = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones_tensor = torch.FloatTensor(dones).to(self.device)

        # Predict Q-values for current states
        q_values = self.network(states_tensor)
        q_values = q_values.gather(1, actions_tensor.unsqueeze(1)).squeeze(1)

        # Target Q-values: r + γ max Q(s', a')
        next_q_values = self.network(next_states_tensor)
        max_next_q_values = next_q_values.max(dim=1)[0]
        target_q_values = rewards_tensor + self.gamma * max_next_q_values * (1 - dones_tensor)

        # MSE loss
        loss = self.loss_fn(q_values, target_q_values.detach())

        # Backprop
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def decay_epsilon(self) -> None:
        """Decrease exploration rate."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def train(self, env, episodes: int = 500, verbose: bool = True) -> Dict:
        """Train DQN agent.

        Args:
            env: CityEnv environment
            episodes: Number of training episodes
            verbose: Print progress

        Returns:
            Dictionary with training metrics
        """
        for episode in range(episodes):
            state, _ = env.reset()
            episode_reward = 0.0
            episode_trips = 0

            for step in range(env.max_steps):
                # Select action
                action = self.select_action(state, training=True)

                # Take action
                next_state, reward, terminated, truncated, info = env.step(action)

                # Store in replay buffer
                done = terminated or truncated
                self.remember(state, action, reward, next_state, done)

                # Train network
                loss = self.replay()

                episode_reward += reward
                if info["trip_obtained"]:
                    episode_trips += 1

                state = next_state

                if done:
                    break

            # Decay exploration
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
        }

    def get_best_action(self, state: np.ndarray) -> int:
        """Get best action (pure exploitation).

        Args:
            state: Current observation

        Returns:
            Best action
        """
        return self.select_action(state, training=False)
