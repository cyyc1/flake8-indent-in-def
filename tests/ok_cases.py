case_0 = ''  # trivial case: no code at all


case_1a = """
def some_func(
        arg1,
        arg2,
        arg3):
    pass
"""


case_1b = """
def some_func(
        arg1,
        arg2,
        arg3,
):
    pass
"""


case_1c = """
def some_func(
        arg1,
        arg2,
        arg3   # trailing comma is not the concern of this plugin
):
    pass
"""


case_1d = """
def some_func(
        arg1: int,
        arg2: str,
        arg3: list,
):
    pass
"""


case_1e = """
def run(
        arg1,  # this looks strange but it is the correct style
        arg2,
        arg3_with_long_name,
):
    pass
"""


case_2a = """
def some_func(
        arg1, arg2=3, arg3=None,
):
    pass
"""


case_2b = """
def some_func(
        arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8,
        a, b, c, d, e, f, g, h, i, j, k,
        x, y, z,
):
    pass
"""


case_2c = """
def some_func(
        arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, a, b, c, d, e, f, g, h, i, j, k, x, y, z,  # noqa: E501
):
    pass
"""


case_2d = """
def some_func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, a, b, c, d, e, f, g, h, i, j, k, x, y, z):  # noqa: E501
    pass
"""


case_4a = """
class MyClass(BaseClassA, BaseClassB, BaseClassC):
    pass
"""


case_4b = """
class MyClass(
        BaseClassA, BaseClassB, BaseClassC,
):
    def __init__(self):
        pass
"""


case_4c = """
class MyClass(
        BaseClassA,
        BaseClassB,
        BaseClassC,
):
    def __init__(self):
        pass
"""


case_5a = """
def func5a(*, arg1, arg2):
    print(1)
"""


case_5b = """
def func5b(
        *,
        arg2,
        arg3,
):
    print(1)
"""


case_5c = """
def func5c(
        *, arg2, arg3,
):
    print(1)
"""


case_5d = """
def func5d(
        arg1,
        arg2='hello',
        *,
        arg3,
        arg4):
    print(2)
"""


case_5e = """
def func5e(
        arg1, 
        arg2,
        *, 
        arg3, 
        **arg4,
):
    print(2)
"""

# Note: there's no case 6. This is to better match "no OK cases"

case_7a = """
def func7a_1():
    def func7a_2():
        def func7a_3():
            def func_7a_4(
                    arg1,
                    arg2,
                    arg3,
            ):
                print(4)
            print(3)
        print(2)
    print(1)                
"""


case_7b = """
def func7b_1():
    def func7b_2(arg1, *, arg2, arg3):
        def func7b_3(
                arg1, arg2, *, arg3):
            def func_7b_4(
                    arg1,
                    arg2,
                    arg3,
            ):
                def func_7b_5():
                    print(5)
                print(4)
            print(3)
        print(2)
    print(1)
"""


def collect_all_cases():
    return (
        case_0,
        case_1a,
        case_1b,
        case_1c,
        case_1d,
        case_1e,
        case_2a,
        case_2b,
        case_2c,
        case_2d,
        case_4a,
        case_4b,
        case_4c,
        case_5a,
        case_5b,
        case_5c,
        case_5d,
        case_5e,
        case_7a,  # There's no case 6. This is to better match "no OK cases"
        case_7b,
    )
