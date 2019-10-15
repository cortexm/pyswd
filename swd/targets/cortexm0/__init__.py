"""Swd package
"""

from swd.targets.cortexm0.stm32f0 import Stm32f0

DEVICES = [
    Stm32f0,
]

__all__ = [
    "Stm32f0"
]
