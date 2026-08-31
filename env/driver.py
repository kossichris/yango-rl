from dataclasses import dataclass, field


@dataclass
class Driver:
    """Represents the driver state and metrics."""
    x: float
    y: float
    total_revenue: float = 0.0
    completed_trips: int = 0
    idle_time: float = 0.0
