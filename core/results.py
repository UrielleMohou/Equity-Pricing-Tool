from dataclasses import dataclass 

@dataclass(frozen=True)
class PricingResult:
    price: float
    delta: float
    gamma: float
    vega: float
    theta: float
    rho: float