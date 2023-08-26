from .a import A_Base
from .b import B_Base

__all__ = ["A", "B"]


class A(A_Base):
    def check(self, value) -> bool:
        return isinstance(value, B)


class B(B_Base):
    def check(self, value) -> bool:
        return isinstance(value, A)
