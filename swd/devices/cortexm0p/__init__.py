"""Cortex-M0+ package
"""

from swd.devices.cortexm0p.stm32g0 import Stm32g0
from swd.devices.cortexm0p.stm32l0 import Stm32l0

CORE = "Cortex-M0+"

FAMILIES = [
    Stm32g0,
    Stm32l0,
]

__all__ = [
    "Stm32g0",
    "Stm32l0",
]
