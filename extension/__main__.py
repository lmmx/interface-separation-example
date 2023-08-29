from extension import interface

a = interface.A()
b = interface.B()

print(f"{a.foo()=}")
print(f"{b.bar()=}")

print(f"{a.check(b)=}")
print(f"{b.check(a)=}")
