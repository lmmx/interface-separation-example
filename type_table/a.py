from typing import Type, ClassVar

from pydantic import BaseModel

__all__ = ["A_Base"]


class A_Base(BaseModel):
    TYPE_TABLE: ClassVar[Type]

    def check(self, value) -> bool:
        return isinstance(value, self.TYPE_TABLE.B)

    def foo(self):
        return "foo"
