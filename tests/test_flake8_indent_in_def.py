import os
import ast
import sys
import pytest
from typing import Set

from flake8_indent_in_def import Plugin

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(THIS_DIR)

import ok_cases  # noqa: E402
import not_ok_cases  # noqa: E402


def _results(src_code: str) -> Set[str]:
    tree = ast.parse(src_code)
    plugin = Plugin(tree)
    return {
        f'{line}:{col} {msg}' for line, col, msg, _ in plugin.run()
    }


@pytest.mark.parametrize('src_code', ok_cases.collect_all_cases())
def test_ok_cases(src_code):
    assert _results(src_code) == set()


@pytest.mark.parametrize(
    'src_code,violation_info',
    not_ok_cases.collect_all_cases(),
)
def test_not_ok_cases(src_code, violation_info):
    expected_violation_messages = {
        f'{line}:{col} {violation_msg}'
        for line, col, violation_msg in violation_info
    }
    assert _results(src_code) == expected_violation_messages
