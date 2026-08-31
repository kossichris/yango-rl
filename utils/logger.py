"""TensorBoard logging utilities."""

from torch.utils.tensorboard import SummaryWriter
from typing import Optional


class RLLogger:
    """Logger for RL training with TensorBoard."""

    def __init__(self, log_dir: str = "runs"):
        """Initialize logger.

        Args:
            log_dir: Directory to save tensorboard logs
        """
        self.writer = SummaryWriter(log_dir=log_dir)
        self.episode = 0

    def log_episode(
        self,
        episode: int,
        reward: float,
        trips: int,
        epsilon: Optional[float] = None,
        loss: Optional[float] = None,
    ) -> None:
        """Log episode metrics.

        Args:
            episode: Episode number
            reward: Episode total reward
            trips: Number of trips obtained
            epsilon: Exploration rate (optional)
            loss: Training loss (optional)
        """
        self.writer.add_scalar("reward/episode", reward, episode)
        self.writer.add_scalar("trips/episode", trips, episode)

        if epsilon is not None:
            self.writer.add_scalar("epsilon", epsilon, episode)

        if loss is not None:
            self.writer.add_scalar("loss", loss, episode)

    def log_evaluation(
        self,
        step: int,
        agent_name: str,
        avg_reward: float,
        std_reward: float,
        avg_trips: float,
        std_trips: float,
    ) -> None:
        """Log evaluation metrics.

        Args:
            step: Step/episode number
            agent_name: Name of agent (Q-Learning, DQN, Random)
            avg_reward: Average reward
            std_reward: Standard deviation of reward
            avg_trips: Average trips
            std_trips: Standard deviation of trips
        """
        self.writer.add_scalar(f"eval/{agent_name}/avg_reward", avg_reward, step)
        self.writer.add_scalar(f"eval/{agent_name}/std_reward", std_reward, step)
        self.writer.add_scalar(f"eval/{agent_name}/avg_trips", avg_trips, step)
        self.writer.add_scalar(f"eval/{agent_name}/std_trips", std_trips, step)

    def flush(self) -> None:
        """Flush logs to disk."""
        self.writer.flush()

    def close(self) -> None:
        """Close writer."""
        self.writer.close()
