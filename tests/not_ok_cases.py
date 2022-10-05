from flake8_indent_in_def import IND101, IND102, IND201, IND202


case_1a_src = """
def some_func(arg1,
              arg2,
              arg3,):
    pass
"""
case_1a = (
    case_1a_src,
    [(3, 14, IND101), (3, 14, IND102), (4, 14, IND101), (4, 14, IND102)],
)


case_1a_alt_src = """
def some_func(arg1: int,
              arg2: dict,
              arg3: bool = False,):
    pass
"""
case_1a_alt = (
    case_1a_alt_src,
    [(3, 14, IND101), (3, 14, IND102), (4, 14, IND101), (4, 14, IND102)],
)


case_1b_src = """
def some_func(arg1,
                arg2,
          arg3):
    pass
"""
case_1b = (
    case_1b_src,
    [(3, 16, IND101), (3, 16, IND102), (4, 10, IND101), (4, 10, IND102)],
)


case_1c_src = """
def some_func(arg1,
                arg2,
                  arg3):
    pass
"""
case_1c = (
    case_1c_src,
    [(3, 16, IND101), (3, 16, IND102), (4, 18, IND101), (4, 18, IND102)],
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
    [(3, 8, IND102), (4, 8, IND102), (5, 8, IND102)],
)


case_1e_src = """
def some_func(arg1, arg2, arg3, arg4, arg5,
              arg6):
    pass
"""
case_1e = (case_1e_src, [(3, 14, IND101), (3, 14, IND102)])


case_1f_src = """
def some_func(arg1, arg2, arg3, arg4, arg5,
        arg6):  # exactly 8 spaces indented, but it's still wrong
    pass
"""
case_1f = (case_1f_src, [(3, 8, IND102)])


case_1g_src = """  # (comes from: https://peps.python.org/pep-0008/#indentation)
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
"""
case_1g = (case_1g_src, [(3, 4, IND101), (4, 4, IND101)])


case_2a_src = """
def some_func(
    arg1,
    arg2,
    arg3):
    pass
"""
case_2a = (case_2a_src, [(3, 4, IND101), (4, 4, IND101), (5, 4, IND101)])


case_2b_src = """
def some_func(
    arg1,
    arg2,
    arg3,
) -> None:
    pass
"""
case_2b = (case_2b_src, [(3, 4, IND101), (4, 4, IND101), (5, 4, IND101)])


case_2c_src = """
def some_func(
      arg1,
      arg2,
      arg3):
    pass
"""
case_2c = (case_2c_src, [(3, 6, IND101), (4, 6, IND101), (5, 6, IND101)])


case_2d_src = """
def some_func(
  arg1,
  arg2,
  arg3):
    pass
"""
case_2d = (case_2d_src, [(3, 2, IND101), (4, 2, IND101), (5, 2, IND101)])


case_2e_src = """
def some_func(
            arg1,
            arg2,
            arg3):
    pass
"""
case_2e = (case_2e_src, [(3, 12, IND101), (4, 12, IND101), (5, 12, IND101)])


case_2f_src = """
def some_func(
    arg1, arg2=1, arg3=None,
):
    pass
"""
case_2f = (case_2f_src, [(3, 4, IND101)])


case_2g_src = """
def some_func(
        arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8,
    a, b, c, d, e, f, g, h, i, j, k,
        x, y, z,
):
    pass
"""
case_2g = (case_2g_src, [(4, 4, IND101)])


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
        (3, 4, IND101),
        (3, 4, IND102),
        (3, 8, IND102),
        (3, 12, IND102),
        (4, 8, IND102),
        (4, 12, IND102),
        (4, 16, IND102),
    ],
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
    [(3, 14, IND101), (3, 14, IND102), (5, 20, IND101), (5, 20, IND102)],
)


case_4a_src = """
class MyClass(BaseClassA,
              BaseClassB,
              BaseClassC):
    pass
"""
case_4a = (
    case_4a_src,
    [(3, 14, IND201), (3, 14, IND202), (4, 14, IND201), (4, 14, IND202)],
)


case_4b_src = """
class MyClass(
    BaseClassA,
    BaseClassB,
    BaseClassC):
    def __init__(self):
        pass
"""
case_4b = (
    case_4b_src,
    [(3, 4, IND201), (4, 4, IND201), (5, 4, IND201)],
)


case_4c_src = """
class MyClass(
    BaseClassA,
    BaseClassB,
    BaseClassC,
):
    def __init__(self):
        pass
"""
case_4c = (
    case_4c_src,
    [(3, 4, IND201), (4, 4, IND201), (5, 4, IND201)],
)


case_4d_src = """
class MyClass(
    BaseClassA, BaseClassB,
    BaseClassC,
):
    def __init__(self):
        pass
"""
case_4d = (
    case_4d_src,
    [(3, 4, IND201), (4, 4, IND201)],
)


case_4e_src = """
class MyClass(
    BaseClassA, BaseClassB, BaseClassC,
):
    def __init__(self):
        pass
"""
case_4e = (case_4e_src, [(3, 4, IND201)])


case_4f_src = """
class MyClass(
    BaseClassA, BaseClassB, BaseClassC,
):
    def __init__(self, arg1, arg2, arg3,
                 arg4,
                 arg5):
        pass
"""
case_4f = (
    case_4f_src,
    [
        (3, 4, IND201),
        (6, 17, IND101),
        (6, 17, IND102),
        (7, 17, IND101),
        (7, 17, IND102),
    ],
)

# There's no case_5a for legacy reasons
case_5b_src = """
def func5b(
    arg5b1,
    *arg5b2,
    **arg5b3,
):
    pass
"""
case_5b = (
    case_5b_src,
    [
        (3, 4, IND101),
        (4, 4, IND101),
        (5, 4, IND101),
    ],
)


case_5c_src = """
def func5c(arg5c1,
           arg5c2,
           *arg5c3,
           **arg5c4):
    pass
"""
case_5c = [
    case_5c_src,
    [
        (3, 11, IND101), (3, 11, IND102),
        (4, 11, IND101), (4, 11, IND102),
        (5, 11, IND101), (5, 11, IND102),
    ],
]


case_5d_src = """
def func5d(arg5d1, arg5d2,
           *arg5d3,
           **arg5d4):
    pass
"""
case_5d = [
    case_5d_src,
    [
        (3, 11, IND101), (3, 11, IND102),
        (4, 11, IND101), (4, 11, IND102),
    ],
]


case_5e_src = """
def func5e(arg5e1, arg5e2,
        *arg5e3,
        **arg5e4,
):
    pass
"""
case_5e = [
    case_5e_src,
    [
        (3, 8, IND102),
        (4, 8, IND102),
    ],
]


case_6a_src = """
def func6a(
    arg6a1,
    *,
    arg6a2,
    arg6a3,
):
    pass
"""
case_6a = (
    case_6a_src,
    [
        (3, 4, IND101),
        (4, 4, IND101),
        (5, 4, IND101),
        (6, 4, IND101),
    ],
)


case_6b_src = """
def func6b(
        arg6b1,
    *,
        arg6b2,
        arg6b3,
):
    pass
"""
case_6b = (
    case_6b_src, [(4, 4, IND101)],
)


case_6c_src = """
def func6c(
    arg6c1,
    *, arg6c2, arg6c3,
):
    pass
"""
case_6c = (
    case_6c_src, [(3, 4, IND101), (4, 4, IND101)],
)


case_6d_src = """
def func6d(
    arg6d1, *,
    arg6d2, arg6d3,
):
    pass
"""
case_6d = (
    case_6d_src, [(3, 4, IND101), (4, 4, IND101)],
)


case_6e_src = """
def func6e(arg6e1, *,
    arg6e2, arg6e3,
):
    pass
"""
case_6e = (
    case_6e_src, [(3, 4, IND101), (3, 4, IND102), (3, 12, IND102)],
)


case_6f_src = """
def func6f(*,
    arg6f2, arg6f3,
):
    pass
"""
case_6f = (
    case_6f_src, [(3, 4, IND101), (3, 4, IND102), (3, 12, IND102)],
)


case_6g_src = """
def func6g(
    *,
    arg6g2, arg6g3,
):
    pass
"""
case_6g = (
    case_6g_src, [(3, 4, IND101), (4, 4, IND101)],
)


case_6h_src = """
def func6h(
    *,
    arg6h2,
    arg6h3,
):
    pass
"""
case_6h = (
    case_6h_src, [(3, 4, IND101), (4, 4, IND101), (5, 4, IND101)],
)


case_6i_src = """
def func6i(
    arg1, 
    arg2,
    *, 
    arg3, 
    **arg4,
):
    print(2)
"""
case_6i = (
    case_6i_src,
    [
        (3, 4, IND101),
        (4, 4, IND101),
        (5, 4, IND101),
        (6, 4, IND101),
        (7, 4, IND101),
    ],
)


case_6j_src = """
def func6j(
    arg1, 
    arg2,
    *, arg3, 
    **arg4,
):
    print(2)
"""
case_6j = (
    case_6j_src, [(3, 4, IND101), (4, 4, IND101), (5, 4, IND101), (6, 4, IND101)],
)


case_7a_src = """
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
case_7a = (
    case_7a_src, [(6, 16, IND101), (7, 16, IND101), (8, 16, IND101)],
)


case_7b_src = """
def func7b_1():
    def func7b_2(arg1,
        *, arg2, arg3):
        def func7b_3(arg1,
                     arg2,
                     *,
                     arg3):
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
case_7b = (
    case_7b_src,
    [
        (4, 8, IND101), (4, 8, IND102), (4, 11, IND102), (4, 17, IND102),
        (6, 21, IND101), (7, 21, IND101), (8, 21, IND101),
        (6, 21, IND102), (7, 21, IND102), (8, 21, IND102),
        (10, 16, IND101), (11, 16, IND101), (12, 16, IND101),
    ],
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
        case_4a,
        case_4b,
        case_4c,
        case_4d,
        case_4e,
        case_4f,
        case_5b,
        case_5c,
        case_5d,
        case_5e,
        case_6a,
        case_6b,
        case_6c,
        case_6d,
        case_6e,
        case_6f,
        case_6g,
        case_6h,
        case_6i,
        case_6j,
        case_7a,
        case_7b,
    )
