import ast
from typing import Generator, Tuple, Type, Any, List, Union

import importlib.metadata as importlib_metadata

IND001 = 'IND001 hanging indentation in function/class definition must be 8 spaces'  # noqa: E501
IND002 = (
    'IND002 if the 1st argument is on the same line as the function/class '
    + 'name, all arguments must be on the same line'
)

EXPECTED_INDENT = 8  # https://peps.python.org/pep-0008/#indentation


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: List[Tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if len(node.args.args) > 0:
            def_line_num = node.lineno
            def_col_offset = node.col_offset

            if node.args.args[0].lineno == def_line_num:
                for this_arg in node.args.args[1:]:
                    if this_arg.lineno != def_line_num:
                        self.violations.append(
                            (this_arg.lineno, this_arg.col_offset + 1, IND002),
                        )

            for i, this_arg in enumerate(node.args.args):
                if i == 0:
                    prev_arg_line_num = def_line_num
                else:
                    prev_arg_line_num = node.args.args[i - 1].lineno

                # Only enforce indentation when this arg is on a new line
                if this_arg.lineno > prev_arg_line_num:
                    if this_arg.col_offset - def_col_offset != EXPECTED_INDENT:
                        self.violations.append(
                            (this_arg.lineno, this_arg.col_offset + 1, IND001),
                        )

            self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col, msg in visitor.violations:
            yield line, col, msg, type(self)
