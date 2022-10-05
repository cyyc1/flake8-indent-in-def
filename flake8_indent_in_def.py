import ast
import tokenize
from enum import Enum
from typing import Generator, Tuple, Type, Any, List, Union, Dict, Optional

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

OP_TOKEN_CODE = 54  # "OP" means operator token
NL_TOKEN_CODE = 61  # "NL" means new line
NEWLINE_TOKEN_CODE = 4


class ArgType(Enum):
    REGULAR = 1
    POS_ONLY = 2
    KW_ONLY = 3
    VARARG = 4
    KWARG = 5


class Visitor(ast.NodeVisitor):
    def __init__(self, tokens: List[tokenize.TokenInfo]) -> None:
        self._tokens: List[tokenize.TokenInfo] = tokens
        self.violations: List[Tuple[int, int, str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        sorted_args, arg_type_lookup, has_star = self._collect_func_args(node)
        if has_star:
            self._visit_node_with_star_in_arg_list(node)
        else:
            self._visit_func_args_or_class_bases(
                node=node,
                args_or_bases=sorted_args,
                is_func=True,
                arg_type_lookup=arg_type_lookup,
            )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._visit_func_args_or_class_bases(node, node.bases, is_func=False)

    @classmethod
    def _collect_func_args(
            cls,
            node: ast.FunctionDef,
    ) -> Tuple[List, Dict[ast.arg, ArgType], bool]:
        """Collect all args from function def; detect presence of * argument"""
        all_args: List[ast.arg] = []
        arg_type_lookup: Dict[ast.arg, ArgType] = {}

        has_star = False  # it means there's a '*,' in the argument list

        if node.args.args:  # List[ast.arg]
            all_args.extend(node.args.args)
            for arg_ in node.args.args:
                arg_type_lookup[arg_] = ArgType.REGULAR

        if node.args.posonlyargs:  # List[ast.arg]
            has_star = True
            all_args.extend(node.args.posonlyargs)
            for arg_ in node.args.posonlyargs:
                arg_type_lookup[arg_] = ArgType.POS_ONLY

        if node.args.kwonlyargs:  # List[ast.arg]
            has_star = True
            all_args.extend(node.args.kwonlyargs)
            for arg_ in node.args.kwonlyargs:
                arg_type_lookup[arg_] = ArgType.KW_ONLY

        if node.args.vararg is not None:
            all_args.append(node.args.vararg)
            arg_type_lookup[node.args.vararg] = ArgType.VARARG

        if node.args.kwarg is not None:
            all_args.append(node.args.kwarg)
            arg_type_lookup[node.args.kwarg] = ArgType.KWARG

        sorted_args = sorted(all_args, key=lambda x: x.lineno, reverse=False)

        return sorted_args, arg_type_lookup, has_star

    def _visit_func_args_or_class_bases(
            self,
            node: Union[ast.FunctionDef, ast.ClassDef],
            args_or_bases: Union[List[ast.arg], List[ast.Name]],
            is_func: bool,
            arg_type_lookup: Optional[Dict[ast.arg, ArgType]] = None,
    ) -> None:
        if is_func:
            code01 = IND101
            code02 = IND102
        else:
            code01 = IND201
            code02 = IND202

        if len(args_or_bases) > 0:
            function_def_line_num = node.lineno
            def_col_offset = node.col_offset

            if args_or_bases[0].lineno == function_def_line_num:
                for item in args_or_bases[1:]:
                    if item.lineno != function_def_line_num:
                        arg_type = arg_type_lookup[item] if is_func else None
                        col_offset = self._calc_col_offset(item, arg_type)
                        self.violations.append((item.lineno, col_offset, code02))

            for i, item in enumerate(args_or_bases):
                if i == 0:
                    prev_item_line_num = function_def_line_num
                else:
                    prev_item_line_num = args_or_bases[i - 1].lineno

                # Only enforce indentation when this arg is on a new line
                if item.lineno > prev_item_line_num:
                    arg_type = arg_type_lookup[item] if is_func else None
                    if self._not_expected_indent(item, def_col_offset, arg_type):
                        col_offset = self._calc_col_offset(item, arg_type)
                        self.violations.append((item.lineno, col_offset, code01))

        # Place this line OUTSIDE `if len(args_or_bases) > 0`, otherwise
        # nested functions/classes will not be detected if the parent function
        # has an empty input argument list
        self.generic_visit(node)

    @classmethod
    def _calc_col_offset(
            cls,
            item: Union[ast.arg, ast.Name],
            arg_type: Optional[ArgType] = None,
    ) -> int:
        if isinstance(item, ast.Name):  # this means base class
            return item.col_offset

        arg_type = ArgType.REGULAR if arg_type is None else arg_type
        return cls._calc_col_offset_for_func_args(item, arg_type)

    @classmethod
    def _calc_col_offset_for_func_args(
            cls,
            arg_: ast.arg,
            arg_type: ArgType,
    ) -> int:
        if arg_type in {ArgType.REGULAR, ArgType.POS_ONLY, ArgType.KW_ONLY}:
            return arg_.col_offset

        if arg_type == ArgType.VARARG:
            return arg_.col_offset - 1  # '-1' because of '*' before vararg

        if arg_type == ArgType.KWARG:
            return arg_.col_offset - 2  # '-2' because of '**' before kwarg

    @classmethod
    def _not_expected_indent(
            cls,
            item: Union[ast.arg, ast.Name],
            def_col_offset: int,
            arg_type: Optional[ArgType] = None,
    ) -> bool:
        if isinstance(item, ast.Name):  # this means base class
            return item.col_offset - def_col_offset != EXPECTED_INDENT

        arg_type = ArgType.REGULAR if arg_type is None else arg_type
        if arg_type in {ArgType.REGULAR, ArgType.POS_ONLY, ArgType.KW_ONLY}:
            expected_indent_ = EXPECTED_INDENT
        elif arg_type == ArgType.VARARG:
            expected_indent_ = EXPECTED_INDENT + 1  # because '*vararg'
        elif arg_type == ArgType.KWARG:
            expected_indent_ = EXPECTED_INDENT + 2  # because '**kwarg'
        else:
            # this branch can't be reached in theory
            expected_indent_ = EXPECTED_INDENT

        return item.col_offset - def_col_offset != expected_indent_

    def _visit_node_with_star_in_arg_list(self, node: ast.FunctionDef) -> None:
        """
        Within this method, we add '*' as an argument into the node's AST
        structure. Somehow, Python stdlib `ast` omits the standalone '*' when
        parsing Python code. Therefore we have to find '*' by tokens and
        manually add it to the structure, as if it were a regular argument.
        """
        func_def_lineno = node.lineno
        func_end_lineno = node.end_lineno

        # We skip the last 2 tokens because the last token from the tokenizer
        # is always ENDMARKER (type 0) and '*' cannot be the 2nd to last token.
        # And then we also skip the 0th token because that is always
        # the ENCODING token (type 62).
        for i in range(1, len(self._tokens) - 2):
            this_token = self._tokens[i]
            next_token = self._tokens[i + 1]
            next_next_token = self._tokens[i + 2]

            this_lineno = this_token.start[0]
            if func_def_lineno <= this_lineno <= func_end_lineno:
                if self._is_qualifying_star(
                    this=this_token,
                    next=next_token,
                    next_next=next_next_token,
                ):
                    self._replace_args_field(node, this_token)
                    self.visit_FunctionDef(node)
                    return  # because there can only be one '*' in the arg list

    @classmethod
    def _replace_args_field(
            cls,
            node: ast.FunctionDef,
            token: tokenize.TokenInfo,
    ) -> None:
        star_arg = cls._build_arg_obj(token)
        new_args_unsorted = (
            node.args.args  # List[ast.arg]
            + [star_arg]
            + node.args.posonlyargs  # List[ast.arg]
            + node.args.kwonlyargs  # List[ast.arg]
        )

        new_args = sorted(
            new_args_unsorted,
            key=lambda x: (x.lineno, x.col_offset),  # first line, then col
        )

        node.args.posonlyargs = []
        node.args.kwonlyargs = []
        node.args.args = new_args

    @classmethod
    def _build_arg_obj(cls, token: tokenize.TokenInfo) -> ast.arg:
        return ast.arg(
            lineno=token.start[0],
            col_offset=token.start[1],
            end_lineno=token.end[0],
            end_col_offset=token.end[1],
            arg='*',
            annotation=None,
            type_comment=None,
        )

    @classmethod
    def _is_qualifying_star(
            cls,
            this: tokenize.TokenInfo,
            next: tokenize.TokenInfo,
            next_next: tokenize.TokenInfo,
    ):
        return (
            cls._is_star_newline_comma(this=this, next=next, next_next=next_next)
            or cls._is_star_comma(this=this, next=next)
        )

    @classmethod
    def _is_star_comma(
            cls,
            this: tokenize.TokenInfo,
            next: tokenize.TokenInfo,
    ) -> bool:
        return cls._is_star(this) and cls._is_comma(next)

    @classmethod
    def _is_star_newline_comma(
            cls,
            this: tokenize.TokenInfo,
            next: tokenize.TokenInfo,
            next_next: tokenize.TokenInfo,
    ) -> bool:
        return (
            cls._is_star(this)
            and cls._is_newline(next)
            and cls._is_comma(next_next)
        )

    @classmethod
    def _is_star(cls, token: tokenize.TokenInfo) -> bool:
        return token.type == OP_TOKEN_CODE and token.string == '*'

    @classmethod
    def _is_comma(cls, token: tokenize.TokenInfo) -> bool:
        return token.type == OP_TOKEN_CODE and token.string == ','

    @classmethod
    def _is_newline(cls, token: tokenize.TokenInfo) -> bool:
        return (
            token.type in {NL_TOKEN_CODE, NEWLINE_TOKEN_CODE}
            and token.string == '\n'
        )


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(
            self,
            tree: ast.AST,
            file_tokens: List[tokenize.TokenInfo] = None,
    ) -> None:
        self._tree = tree
        self._file_tokens = file_tokens

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor(self._file_tokens)

        visitor.visit(self._tree)
        for line, col, msg in visitor.violations:
            yield line, col, msg, type(self)
