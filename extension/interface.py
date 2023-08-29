from __future__ import annotations

from typing import ClassVar, Type

from .a import A_Base
from .b import B_Base

__all__ = ["A", "B"]


class A(A_Base):
    B: ClassVar[Type[B]]


class B(B_Base):
    A: ClassVar[Type[A]] = A


A.B = B
