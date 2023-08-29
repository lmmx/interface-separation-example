from typing import Type, ClassVar

from pydantic import BaseModel

__all__ = ["B_Base"]


class B_Base(BaseModel):
    TYPE_TABLE: ClassVar[Type]

    def check(self, value) -> bool:
        return isinstance(value, self.TYPE_TABLE.A)

    def bar(self):
        return "bar"
