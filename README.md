# flake8-indent-in-def

This is a [flake8](https://flake8.pycqa.org/en/latest/) plugin enforces 8-space indentation in function/class definitions in Python code.

## Installation

```bash
pip install flake8-indent-in-def
```

## Violation codes

There is one violation code that this plugin reports:

| Code    | Description                                                       |
| ------- | ----------------------------------------------------------------- |
| IND101  | hanging indentation in function definition must be 8 spaces       |
| IND102  | if the 1st argument is on the same line as the function name, all other arguments must be on the same line |
| IND201  | hanging indentation in class definition must be 8 spaces          |
| IND202  | if the 1st base class is on the same line as the class name, all other base classes must be on the same line |


## Style examples

### _Wrong_

This plugin, as well as [PEP8](https://peps.python.org/pep-0008/#indentation), considers the following indentation styles wrong:

```python
def some_function(argument1,
                  argument2,
                  argument3, argument4, argumen5):
    print(argument1)
```

```python
def some_function(arg1,
                  arg2,
                  arg3):
    print(arg1)
```

```python
def some_function(
    arg1: int,
    arg2: list,
    arg3: bool = None,
):
    print(arg1)
```

Note: this style above is the style choice of the [`black` formatter](https://github.com/psf/black). This style is wrong because arguments and function names would be difficult to visually distinghish.

### _Correct_

Correspondingly, here are the correct indentation styles:

```python
def some_function(
        arg1: int,
        arg2: list,
        arg3: bool = None,
):
    print(arg1)
```

```python
def some_function(
        arg1: int, arg2: list, arg3: bool = None
) -> None:
    print(arg1)
```

```python
def some_function(arg1: int, arg2: list, arg3: bool = None) -> None:
    print(arg1)
```

```python
def some_function(
        arg1: int, arg2: list,
        arg3: bool = None, arg4: float = 2.0,
) -> None:
    print(arg1)
```

Additionally, this plugin by default enforces the same indentation styles on class inheritence:

```python
class MyClass(
        BaseClassA,
        BaseClassB,
        BaseClassC,
):
    def __init__(self):
        pass
```
You can opt out of class inheritence checks by ignoring rules `IND201` and `IND202`.

## Rationale

When we only indent by 4 spaces in function definitions, it is difficult to visually distinguish function arguments with the function name and the function body. This reduces readability.

It is similar for base classes in class definitions, but it's less of an issue than function definitions.

## Interaction with other style checkers and formatters

* [`black`](https://github.com/psf/black)-formatted code will cause a style violation here, because `black` authors [explicitly opted for the 4-space indentation and do not plan to change it](https://github.com/psf/black/issues/1178#issuecomment-614050678)
* The style enforced in this plugin contradicts with rule [WPS318](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/consistency.html#wemake_python_styleguide.violations.consistency.ExtraIndentationViolation) enforced by [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide) ("WPS")
    - But WPS is configurable so you can always opt out of WPS318
* This plugin does not check trailing commas, because [flake8-commas](https://github.com/PyCQA/flake8-commas) already does it
* This plugin does not forbid grouping arguments (see example below), because [WPS317](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/consistency.html#wemake_python_styleguide.violations.consistency.ParametersIndentationViolation) can enforce it
```python
def some_func(
        arg1, arg2, arg3,
        arg4, arg5,
):
    pass
```
