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
    )
