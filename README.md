# interface-separation-example

Design demo: letting module structure be led by the coupling of classes in a "class interface",
to minimise use of tricks like lazy imports to avoid cyclic import errors

## :mag: Observation: cyclic import dependencies between classes create 'traffic jams' in code interfaces

- Sometimes classes are interconnected (e.g. one is used in the other's method)
- When this occurs bidirectionally it is awkward, 'hacky' and sometimes impossible to separate them
- These classes will typically get 'frozen' in place (or 'jammed' like traffic)
- As these classes acquire new behaviour, the location of the traffic jam begins to resemble a pile
  up: this is how monoliths are made
- The seemingly simple approach is to keep the class structure 'simple', as it is expected to be
  more intuitive/comprehensible
- This expected ease of understanding is harmed by the code's growth at a single site
- All references to the residents of that module equate their location with their interface
  (use/address distinction collapses for both the package's writers and its users)

## :bulb: Idea 1: extract methods without cyclic dependencies into a base class

- Identify the minimal interface that can be retained without breaking the cyclic dependency
- Expose this 'class interface' as the class structure (guaranteed import cycle-free),
  much like you would expose a 'package interface' (commonly called a package's API) as the module structure
  - In the example `solution` package in this repo, this is `interface.py`
- Existing code with complex interconnected monolithic modules can be simplified down to a core class interface.
- The degree of this interconnection will determine the proportion of a given monolith that can be
  extracted (i.e. how far it can be simplified by this technique)
- It introduces a similar kind of use/address distinction as the 'shallow handler' pattern does for
  CLI entrypoints etc.
  - This is the principle that sites of use should be configurable,
    but not themselves be sites of configuration definition

## :bulb::bulb: Idea 2: extract all methods into a base class by storing type references as class variables

- The only thing holding methods back from being extracted from the minimal interface is that method
  bodies may reference other classes in the namespace
- To relieve these jams we can put the types in class variables: i.e. put the namespace types in the
  data model! They're accessed as data at runtime so they must indeed be considered part of the data model.
  - This is demonstrated in the further example `extension` package in this repo
- The only way to make this work that I can think of is to assign the types to the data models
  they're needed in after the type has been created. Forward references won't work here.
- This would give a completely 'shallow' class in the class interface, with all methods falling
  through to the base class in a standalone module.

### :bulb::bulb::bulb: Idea 3: store the type references in a type table as the class variable access point

- All methods use the same approach to access the type references, and it's more explicit what is happening when an
  object refers to an attribute that shares the name of a class (`self.TYPE_TABLE.A` is clearer than `self.A`)
- This is shown in `type_table`

#### :bulb: Version 4: make the type table a Pydantic model for easy setup via `__class_vars__`

- To minimise the amount of manual setup required to use this pattern (so it scales nicely), set up
  the class variables by a helper method that assigns names from the `interface.py` module namespace.
- This is shown in `type_table_record`
- **Open question**: how can this type table be made immutable at `setup()` time so that runtime types
  cannot be modified?
  - We can't use Pydantic's `validate_assignment` here because class variables are not model fields.
  - There is a breakpoint left in the `__main__.py` to highlight this mutability.

#### :bulb: Version 5: use a mixin as a single point of configuration

- This is my final preference for its brevity and single point of configuration of the `TYPE_TABLE`
  class variable on the classes recorded in the table, using multiple inheritance (a.k.a. mixins).
- With this modification we end up with a system that requires 0 extra lines per class, only the
  inheritance of the `RecordedType` mixin in the classdef line.
- This is shown in `type_table_record_mixin`

In its final form then we have `type_table_record_mixin/interface.py`:

```py
from __future__ import annotations

from typing import ClassVar, Type

from pydantic import BaseModel

from .a import A_Base
from .b import B_Base

__all__ = ["TYPE_TABLE", "TabulatedType", "A", "B"]


class TYPE_TABLE(BaseModel):
    A: ClassVar[Type[A]]
    B: ClassVar[Type[B]]

    @classmethod
    def setup(cls) -> None:
        for classvar in cls.__class_vars__:
            setattr(cls, classvar, globals()[classvar])


class TabulatedType:
    TYPE_TABLE: ClassVar[Type[TYPE_TABLE]] = TYPE_TABLE


class A(TabulatedType, A_Base):
    ...


class B(TabulatedType, B_Base):
    ...


TYPE_TABLE.setup()
```

## Demo

### Problem

Running `python -m demo` gives a traceback due to cyclic import

```sh
Traceback (most recent call last):
...
  File ".../interface-separation-demo/demo/__init__.py", line 1, in
<module>
    from .a import A
  File ".../interface-separation-demo/demo/a.py", line 1, in <module>
    from .b import B
  File ".../interface-separation-demo/demo/b.py", line 1, in <module>
    from .a import A
ImportError: cannot import name 'A' from partially initialized module 'demo.a' (most likely due to a
circular import) (.../interface-separation-demo/demo/a.py)
```

### Solution 1) extract unconnected methods

Running `python -m solution` gives no output (i.e. it works fine: the code executes without circular
import error).

```sh
```

### Solution 2) extract all methods by putting types on the data model

Running `python -m extension` gives output from methods `foo` and `bar` demonstrating that the classes run successfully,
and output from `check` methods on A and B demonstrating runtime access of B within A and vice versa.

```sh
a.foo()='foo'
b.bar()='bar'
a.check(b)=True
b.check(a)=True
```

### Solution 3) use a type table

Running `python -m type_table` gives the same output as above, but using a type table.

### Solution 4) use a Pydantic data model of types for type table setup assistance

Running `python -m type_table_record` is equivalent to the above, but will breakpoint to demonstrate
the mutability of the type table record values.

### Solution 5) use a Pydantic data model of types for type table setup assistance as a mixin

Running `python -m type_table_record_mixin` is equivalent to the above, but uses a mixin to abstract
away the assignment of the `TYPE_TABLE` classvar.
