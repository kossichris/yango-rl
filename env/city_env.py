import gymnasium as gym
import numpy as np
from gymnasium import spaces
from typing import Tuple, Dict, Optional

from .city import City
from .driver import Driver


class CityEnv(gym.Env):
    """Gymnasium environment for driver repositioning optimization.

    State: [x, y, hour, day, idle_time]
    Action: zone_id to move to
    Reward: trip_fare - repositioning_cost
    """

    metadata = {"render_modes": []}

    def __init__(
        self,
        grid_size: int = 5,
        demand_probability: float = 0.5,
        max_steps: int = 1000,
        seed: Optional[int] = None,
    ):
        """
        Args:
            grid_size: City grid size (grid_size x grid_size zones)
            demand_probability: Base probability of trip request per zone
            max_steps: Maximum steps per episode
            seed: Random seed
        """
        self.grid_size = grid_size
        self.demand_probability = demand_probability
        self.max_steps = max_steps
        self.num_zones = grid_size * grid_size

        self.city = City(grid_size=grid_size, base_demand_probability=demand_probability, seed=seed)
        self.driver = Driver(x=0.0, y=0.0)
        self.rng = np.random.RandomState(seed)

        self.current_step = 0

        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0], dtype=np.float32),
            high=np.array([grid_size, grid_size, 24, 7, 1000], dtype=np.float32),
            dtype=np.float32,
        )

        self.action_space = spaces.Discrete(self.num_zones)

    def _get_observation(self) -> np.ndarray:
        """Return state as [x, y, hour, day, idle_time]."""
        hour = self.city.current_time % 24.0
        day = self.city.current_day
        idle_time = min(self.driver.idle_time, 1000.0)
        return np.array([self.driver.x, self.driver.y, hour, day, idle_time], dtype=np.float32)

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[np.ndarray, Dict]:
        """Reset environment to initial state."""
        if seed is not None:
            self.rng = np.random.RandomState(seed)
            self.city = City(grid_size=self.grid_size, base_demand_probability=self.demand_probability, seed=seed)

        self.driver = Driver(x=0.0, y=0.0)
        self.city.reset()
        self.current_step = 0

        obs = self._get_observation()
        return obs, {}

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """Execute one environment step.

        Args:
            action: Zone ID to move to

        Returns:
            obs, reward, terminated, truncated, info
        """
        self.current_step += 1
        terminated = self.current_step >= self.max_steps

        target_zone_id = int(np.clip(action, 0, self.num_zones - 1))
        target_zone = self.city.get_zone(target_zone_id)

        travel_distance = np.sqrt((self.driver.x - target_zone.x) ** 2 + (self.driver.y - target_zone.y) ** 2)
        travel_cost = travel_distance * self.city.cost_per_km

        self.driver.x = target_zone.x
        self.driver.y = target_zone.y
        self.driver.total_revenue -= travel_cost
        self.driver.idle_time = 0.0

        trip = self.city.request_trip(target_zone)
        reward = -travel_cost

        if trip is not None:
            self.driver.total_revenue += trip.fare
            self.driver.completed_trips += 1
            reward += trip.fare
        else:
            self.driver.idle_time += 1.0

        self.city.step(time_delta=1.0)

        obs = self._get_observation()
        info = {
            "x": self.driver.x,
            "y": self.driver.y,
            "total_revenue": self.driver.total_revenue,
            "completed_trips": self.driver.completed_trips,
            "trip_obtained": trip is not None,
        }

        return obs, float(reward), terminated, False, info

    def render(self):
        """Render current state."""
        print(
            f"Step {self.current_step}: ({self.driver.x:.1f}, {self.driver.y:.1f}), "
            f"Revenue: {self.driver.total_revenue:.2f}, Trips: {self.driver.completed_trips}"
        )
