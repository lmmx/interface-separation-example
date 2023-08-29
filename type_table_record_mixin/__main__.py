from . import interface

a = interface.A()
b = interface.B()

print(f"{a.foo()=}")
print(f"{b.bar()=}")

print(f"{a.check(b)=}")
print(f"{b.check(a)=}")

# I don't know how to make the type table immutable (i.e. how not to reach the breakpoint below)
try:
    interface.TYPE_TABLE.A = None
except:
    print("Override errored: right")
else:
    breakpoint()
    print("Did not error: wrong")
