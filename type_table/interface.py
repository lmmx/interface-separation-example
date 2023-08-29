from __future__ import annotations

from typing import ClassVar, Type

from .a import A_Base
from .b import B_Base

__all__ = ["TYPE_TABLE", "A", "B"]


class TYPE_TABLE:
    A: ClassVar[Type[A]]
    B: ClassVar[Type[B]]


class A(A_Base):
    TYPE_TABLE: ClassVar[Type[TYPE_TABLE]] = TYPE_TABLE


class B(B_Base):
    TYPE_TABLE: ClassVar[Type[TYPE_TABLE]] = TYPE_TABLE


TYPE_TABLE.A = A
TYPE_TABLE.B = B
