import math
import numpy as np

from core.products import VanillaOption


def intrinsic_value(spot: float | np.ndarray, strike: float, option_type: str):
    if option_type == "call":
        return np.maximum(spot - strike, 0.0)
    return np.maximum(strike - spot, 0.0)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bermudan_exercise_indices(option: VanillaOption, steps: int) -> set[int]:
    if option.exercise_style == "european":
        return {steps}
    if option.exercise_style == "american":
        return set(range(1, steps + 1))

    dates = option.bermudan_dates
    raw = np.linspace(1, steps, dates, dtype=int)
    return set(int(i) for i in raw.tolist())
