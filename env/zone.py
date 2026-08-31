from dataclasses import dataclass
import numpy as np


@dataclass
class Zone:
    """Represents a zone in the city with geographical and demand characteristics."""
    zone_id: int
    name: str
    x: float
    y: float
    demand_probability: float = 0.5

    def distance_to(self, other: "Zone") -> float:
        """Euclidean distance to another zone."""
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
