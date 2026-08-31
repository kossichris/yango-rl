import numpy as np
import random
from typing import List, Optional
from .zone import Zone
from .trip import Trip


class City:
    """Represents the city with zones, geography, and demand simulation."""

    def __init__(
        self,
        grid_size: int = 5,
        base_demand_probability: float = 0.5,
        seed: Optional[int] = None,
    ):
        """
        Args:
            grid_size: Number of zones per side (grid_size x grid_size)
            base_demand_probability: Base probability of trip request per zone
            seed: Random seed for reproducibility
        """
        self.grid_size = grid_size
        self.num_zones = grid_size * grid_size
        self.base_demand_probability = base_demand_probability
        self.rng = np.random.RandomState(seed)
        if seed is not None:
            random.seed(seed)

        self.zones = self._create_zones()

        self.current_time = 0.0
        self.current_day = 0
        self.cost_per_km = 0.1

    def _create_zones(self) -> List[Zone]:
        """Create a grid of zones with demand characteristics."""
        zones = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                zone_id = i * self.grid_size + j
                zone_name = f"{chr(65 + i)}{j}"  # A0, A1, B0, B1, etc.
                x, y = float(i), float(j)
                demand_prob = self.base_demand_probability + 0.1 * self.rng.randn()
                demand_prob = max(0.1, min(0.9, demand_prob))  # Clamp to [0.1, 0.9]
                zones.append(Zone(zone_id, zone_name, x, y, demand_prob))
        return zones

    def get_zone(self, zone_id: int) -> Zone:
        """Get a zone by ID."""
        return self.zones[zone_id]

    def generate_trip(self, pickup_zone: Zone) -> Trip:
        """Generate a trip from a pickup zone to a random destination.

        Args:
            pickup_zone: The zone where the trip originates

        Returns:
            Trip with random destination, fare, and distance
        """
        dropoff_zone = random.choice(self.zones)
        distance = pickup_zone.distance_to(dropoff_zone)
        fare = random.uniform(1500, 5000)

        return Trip(
            pickup_zone=pickup_zone.name,
            dropoff_zone=dropoff_zone.name,
            fare=fare,
            distance=distance,
        )

    def request_trip(self, zone: Zone) -> Optional[Trip]:
        """Request a trip in a given zone.

        Returns a Trip if a client appears (based on zone demand probability),
        None otherwise.

        Args:
            zone: The zone where the trip is requested

        Returns:
            Trip if client appears, None otherwise
        """
        demand_prob = zone.demand_probability
        if random.random() < demand_prob:
            return self.generate_trip(zone)
        return None

    def step(self, time_delta: float = 1.0):
        """Advance simulation time."""
        self.current_time += time_delta
        self.current_day = int((self.current_time / 24.0)) % 7

    def reset(self):
        """Reset city time."""
        self.current_time = 0.0
        self.current_day = 0
