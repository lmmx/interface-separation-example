from typing import Type, ClassVar

from pydantic import BaseModel

__all__ = ["A_Base"]


class A_Base(BaseModel):
    B: ClassVar[Type]

    def check(self, value) -> bool:
        return isinstance(value, self.B)

    def foo(self):
        return "foo"
