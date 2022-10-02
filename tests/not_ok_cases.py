from flake8_indent_in_def import IND001, IND002


case_1a_src = """
def some_func(arg1,
              arg2,
              arg3,):
    pass
"""
case_1a = (
    case_1a_src,
    [(3, 15, IND001), (3, 15, IND002), (4, 15, IND001), (4, 15, IND002)],
)


case_1a_alt_src = """
def some_func(arg1: int,
              arg2: dict,
              arg3: bool = False,):
    pass
"""
case_1a_alt = (
    case_1a_alt_src,
    [(3, 15, IND001), (3, 15, IND002), (4, 15, IND001), (4, 15, IND002)],
)


case_1b_src = """
def some_func(arg1,
                arg2,
          arg3):
    pass
"""
case_1b = (
    case_1b_src,
    [(3, 17, IND001), (3, 17, IND002), (4, 11, IND001), (4, 11, IND002)],
)


case_1c_src = """
def some_func(arg1,
                arg2,
                  arg3):
    pass
"""
case_1c = (
    case_1c_src,
    [(3, 17, IND001), (3, 17, IND002), (4, 19, IND001), (4, 19, IND002)],
)


case_1d_src = """
def run(arg1,
        arg2,  # it happens to indent 8 spaces, but this is still wrong
        arg3,
        arg4):
    pass 
"""
case_1d = (
    case_1d_src,
    [(3, 9, IND002), (4, 9, IND002), (5, 9, IND002)],
)


case_1e_src = """
def some_func(arg1, arg2, arg3, arg4, arg5,
              arg6):
    pass
"""
case_1e = (case_1e_src, [(3, 15, IND001), (3, 15, IND002)])


case_1f_src = """
def some_func(arg1, arg2, arg3, arg4, arg5,
        arg6):  # exactly 8 spaces indented, but it's still wrong
    pass
"""
case_1f = (case_1f_src, [(3, 9, IND002)])


case_1g_src = """  # (comes from: https://peps.python.org/pep-0008/#indentation)
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
"""
case_1g = (case_1g_src, [(3, 5, IND001), (4, 5, IND001)])


case_2a_src = """
def some_func(
    arg1,
    arg2,
    arg3):
    pass
"""
case_2a = (case_2a_src, [(3, 5, IND001), (4, 5, IND001), (5, 5, IND001)])


case_2b_src = """
def some_func(
    arg1,
    arg2,
    arg3,
) -> None:
    pass
"""
case_2b = (case_2b_src, [(3, 5, IND001), (4, 5, IND001), (5, 5, IND001)])


case_2c_src = """
def some_func(
      arg1,
      arg2,
      arg3):
    pass
"""
case_2c = (case_2c_src, [(3, 7, IND001), (4, 7, IND001), (5, 7, IND001)])


case_2d_src = """
def some_func(
  arg1,
  arg2,
  arg3):
    pass
"""
case_2d = (case_2d_src, [(3, 3, IND001), (4, 3, IND001), (5, 3, IND001)])


case_2e_src = """
def some_func(
            arg1,
            arg2,
            arg3):
    pass
"""
case_2e = (case_2e_src, [(3, 13, IND001), (4, 13, IND001), (5, 13, IND001)])


case_2f_src = """
def some_func(
    arg1, arg2=1, arg3=None,
):
    pass
"""
case_2f = (case_2f_src, [(3, 5, IND001)])


case_2g_src = """
def some_func(
        arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8,
    a, b, c, d, e, f, g, h, i, j, k,
        x, y, z,
):
    pass
"""
case_2g = (case_2g_src, [(4, 5, IND001)])


case_2h_src = """
def some_func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8,
    a1, b1, c1,
        x1, y1, z1,
):
    pass
"""
case_2h = (
    case_2h_src,
    [
        (3, 5, IND001),
        (3, 5, IND002),
        (3, 9, IND002),
        (3, 13, IND002),
        (4, 9, IND002),
        (4, 13, IND002),
        (4, 17, IND002),
    ]
)


case_3a_src = """
def some_func(arg1,
              arg2):
    def some_func_2(arg1_,
                    arg2_):
        return 1

    return 2
"""
case_3a = (
    case_3a_src,
    [(3, 15, IND001), (3, 15, IND002), (5, 21, IND001), (5, 21, IND002)],
)


def collect_all_cases():
    return (
        case_1a,
        case_1a_alt,
        case_1b,
        case_1c,
        case_1d,
        case_1e,
        case_1f,
        case_1g,
        case_2a,
        case_2b,
        case_2c,
        case_2d,
        case_2e,
        case_2f,
        case_2g,
        case_2h,
        case_3a,
    )
