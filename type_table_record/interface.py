from __future__ import annotations

from typing import ClassVar, Type

from pydantic import BaseModel

from .a import A_Base
from .b import B_Base

__all__ = ["TYPE_TABLE", "A", "B"]


class TYPE_TABLE(BaseModel):
    A: ClassVar[Type[A]]
    B: ClassVar[Type[B]]

    @classmethod
    def setup(cls) -> None:
        for classvar in cls.__class_vars__:
            setattr(cls, classvar, globals()[classvar])


class A(A_Base):
    TYPE_TABLE: ClassVar[Type[TYPE_TABLE]] = TYPE_TABLE


class B(B_Base):
    TYPE_TABLE: ClassVar[Type[TYPE_TABLE]] = TYPE_TABLE


TYPE_TABLE.setup()
