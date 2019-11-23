"""Cortex-M7 package
"""

from swd.targets.cortexm7.stm32h7 import Stm32h7

CORE = "Cortex-M7"

FAMILIES = [
    Stm32h7,
]

__all__ = [
    "Stm32h7",
]
