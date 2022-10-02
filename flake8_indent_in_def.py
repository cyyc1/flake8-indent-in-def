import ast
from typing import Generator, Tuple, Type, Any, List, Union

import importlib.metadata as importlib_metadata

IND101 = 'IND101 hanging indentation in function definition must be 8 spaces'
IND102 = (
    'IND102 if the 1st argument is on the same line as the function '
    + 'name, all other arguments must be on the same line'
)

IND201 = 'IND201 hanging indentation in class definition must be 8 spaces'
IND202 = (
    'IND202 if the 1st base class is on the same line as the class '
    + 'name, all other base classes must be on the same line'
)

EXPECTED_INDENT = 8  # https://peps.python.org/pep-0008/#indentation


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: List[Tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_func_args_or_class_bases(node, node.args.args, is_func=True)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._visit_func_args_or_class_bases(node, node.bases, is_func=False)

    def _visit_func_args_or_class_bases(
            self,
            node: Union[ast.FunctionDef, ast.ClassDef],
            args_or_bases: Union[List[ast.arg], List[ast.Name]],
            is_func: bool,
    ) -> None:
        if is_func:
            code01 = IND101
            code02 = IND102
        else:
            code01 = IND201
            code02 = IND202

        if len(args_or_bases) > 0:
            def_line_num = node.lineno
            def_col_offset = node.col_offset

            if args_or_bases[0].lineno == def_line_num:
                for item in args_or_bases[1:]:
                    if item.lineno != def_line_num:
                        self.violations.append(
                            (item.lineno, item.col_offset + 1, code02),
                        )

            for i, item in enumerate(args_or_bases):
                if i == 0:
                    prev_item_line_num = def_line_num
                else:
                    prev_item_line_num = args_or_bases[i - 1].lineno

                # Only enforce indentation when this arg is on a new line
                if item.lineno > prev_item_line_num:
                    if item.col_offset - def_col_offset != EXPECTED_INDENT:
                        self.violations.append(
                            (item.lineno, item.col_offset + 1, code01),
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
