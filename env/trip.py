from dataclasses import dataclass


@dataclass
class Trip:
    """Represents a single trip/ride."""
    pickup_zone: str
    dropoff_zone: str
    fare: float
    distance: float
