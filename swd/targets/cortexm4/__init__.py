"""Cortex-M4 package
"""

from swd.targets.cortexm4.stm32f3 import Stm32f3
from swd.targets.cortexm4.stm32f4 import Stm32f4
from swd.targets.cortexm4.stm32l4 import Stm32l4

CORE = "Cortex-M4"

FAMILIES = [
    Stm32f3,
    Stm32f4,
    Stm32l4,
]

__all__ = [
    "Stm32f3",
    "Stm32f4",
    "Stm32l4",
]
