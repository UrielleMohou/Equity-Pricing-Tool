from dataclasses import dataclass

@dataclass(frozen=True)
class EuropeanOption:
    strike: float
    maturity: float
    option_type: str

    def validate(self) -> None:
        if self.strike <= 0:
            raise ValueError("strike must be strictly positive.")
        if self.maturity <= 0:
            raise ValueError("maturity must be strictly positive.")
        if self.option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'.")
        