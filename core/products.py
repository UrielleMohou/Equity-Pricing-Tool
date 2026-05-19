from dataclasses import dataclass


@dataclass(frozen=True)
class VanillaOption:
    strike: float
    maturity: float
    option_type: str       # "call" or "put"
    exercise_style: str    # "european", "american", or "bermudan"
    bermudan_dates: int = 4

    def validate(self) -> None:
        if self.strike <= 0:
            raise ValueError("strike must be strictly positive.")
        if self.maturity <= 0:
            raise ValueError("maturity must be strictly positive.")
        if self.option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'.")
        if self.exercise_style not in {"european", "american", "bermudan"}:
            raise ValueError("exercise_style must be 'european', 'american', or 'bermudan'.")
        if self.exercise_style == "bermudan" and self.bermudan_dates < 1:
            raise ValueError("bermudan_dates must be at least 1.")
