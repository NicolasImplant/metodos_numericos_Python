from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneratorMethod(StrEnum):
    MIDDLE_SQUARES = "middle_squares"
    CONSTANT_MULTIPLIER = "constant_multiplier"
    MIDDLE_PRODUCTS = "middle_products"
    LINEAR_CONGRUENTIAL = "linear_congruential"
    MULTIPLICATIVE_CONGRUENTIAL = "multiplicative_congruential"
    ADDITIVE_CONGRUENTIAL = "additive_congruential"
    QUADRATIC_CONGRUENTIAL = "quadratic_congruential"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PRN_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    method: GeneratorMethod = Field(default=GeneratorMethod.LINEAR_CONGRUENTIAL)

    # ── Seed and output size ─────────────────────────────────────────────────
    seed: int = Field(default=1234, ge=1)
    count: int = Field(default=1000, ge=1)

    # ── Congruential parameters ──────────────────────────────────────────────
    multiplier: int = Field(default=0, ge=0)     # a
    increment: int = Field(default=0, ge=0)      # c
    modulus_exponent: int = Field(default=31, ge=1)  # m = 2^g

    # ── Quadratic congruential ───────────────────────────────────────────────
    coeff_a: int = Field(default=3, ge=0)
    coeff_b: int = Field(default=5, ge=0)
    coeff_c: int = Field(default=7, ge=0)

    # ── Additive congruential (lag vector as comma-separated string) ─────────
    lag_vector_str: str = Field(default="1009,2011,3001,4001,5003", alias="PRN_LAG_VECTOR")

    # ── Output and analysis ──────────────────────────────────────────────────
    run_statistics: bool = Field(default=True)
    output_dir: Path = Field(default=Path("output"))
    log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_prefix="PRN_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
    )

    @property
    def modulus(self) -> int:
        return 2 ** self.modulus_exponent

    @property
    def lag_vector(self) -> tuple[int, ...]:
        return tuple(int(x.strip()) for x in self.lag_vector_str.split(",") if x.strip())
