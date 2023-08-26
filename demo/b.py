from .a import A


class B:
    def check(self, value) -> bool:
        return isinstance(value, A)
