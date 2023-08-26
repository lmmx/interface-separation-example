from .b import B


class A:
    def check(self, value) -> bool:
        return isinstance(value, B)
