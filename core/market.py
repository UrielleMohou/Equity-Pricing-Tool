from dataclasses import dataclass

@dataclass(frozen=True)
class MarketData:
    spot: float
    rate: float
    dividend: float
    volatility: float

    def validate(self) -> None:
        if self.spot <= 0:
            raise ValueError("spot must be strictly positive.")
        if self.volatility <= 0:
            raise ValueError("volatility must be strictly positive.")
