from collections import Iterable
from traceback import format_exception
from typing import List, Dict, Any, Optional

from attr import dataclass
from pytezos.michelson.instructions import CommitInstruction
from pytezos.michelson.instructions.base import MichelsonInstruction
from pytezos.michelson.micheline import MichelineSequence, Micheline, MichelsonRuntimeError
from pytezos.michelson.parse import MichelsonParserError
from pytezos.michelson.stack import MichelsonStack
from tabulate import tabulate
from ipykernel.kernelbase import Kernel

from pytezos.michelson.repl import Interpreter, InterpreterResult
from pytezos.michelson.tags import prim_tags
from michelson_kernel import __version__
from michelson_kernel.docs import docs

static_macros = [
    'CMPEQ',
    'CMPNEQ',
    'CMPLT',
    'CMPGT',
    'CMPLE',
    'CMPGE',
    'IFEQ',
    'IFNEQ',
    'IFLT',
    'IFGT',
    'IFLE',
    'IFGE',
    'IFCMPEQ',
    'IFCMPNEQ',
    'IFCMPLT',
    'IFCMPGT',
    'IFCMPLE',
    'IFCMPGE',
    'FAIL',
    'ASSERT_EQ',
    'ASSERT_NEQ',
    'ASSERT_LT',
    'ASSERT_GT',
    'ASSERT_LE',
    'ASSERT_GE',
    'ASSERT_CMPEQ',
    'ASSERT_CMPNEQ',
    'ASSERT_CMPLT',
    'ASSERT_CMPGT',
    'ASSERT_CMPLE',
    'ASSERT_CMPGE',
    'ASSERT_NONE',
    'ASSERT_SOME',
    'ASSERT_LEFT',
    'ASSERT_RIGHT',
    'UNPAIR',
    'IF_SOME',
    'SET_CAR',
    'SET_CDR',
    'MAP_CAR',
    'MAP_CDR',
]


def parse_token(line, cursor_pos):

    begin_pos = next((i + 1 for i in range(cursor_pos - 1, 0, -1) if line[i] in ' ;({\n'), 0)
    end_pos = next((i for i in range(cursor_pos, len(line)) if line[i] in ' ;){\n'), len(line))
    return line[begin_pos:end_pos], begin_pos, end_pos


def preformat_stack_table(items: Iterable[MichelsonInstruction]) -> List[Dict[str, Any]]:
    return [
        {
            'index': i,
            'type': item.prim,
            'value': item.to_python_object(),
        }
        for i, item in enumerate(items)
    ]


def html_table(table: List[Dict[str, Any]]) -> str:
    def pre(s):
        return f'<pre style="text-align: left;">{s}</pre>'

    def pre_dict(d):
        return {k: pre(v) for k, v in d.items()}

    res = tabulate(list(map(pre_dict, table)), tablefmt='html', headers="keys")
    res = res.replace('&lt;', '<').replace('&gt;', '>')  # tabulate escapes our <pre> tags
    return res


def plain_table(table: List[Dict[str, Any]]) -> str:
    return tabulate(table, tablefmt='simple', headers='keys')


@dataclass(kw_only=True)
class CellResult:
    lazy_diff = None
    stack_items = None


class MichelsonKernel(Kernel):
    implementation = 'IMichelson'
    implementation_version = __version__
    language_info = {
        'name': 'Michelson',
        'mimetype': 'text/x-michelson',
        'file_extension': '.tz',
        'codemirror_mode': 'michelson',
    }
    banner = 'Michelson (Tezos VM language)'
    help_links = [
        'https://michelson.nomadic-labs.com/',
        'https://tezos.gitlab.io/whitedoc/michelson.html',
    ]

    def __init__(self, **kwargs):
        super(MichelsonKernel, self).__init__(**kwargs)
        self.interpreter = Interpreter()

    def _stdout(self, text: str) -> None:
        self.send_response(
            self.iopub_socket,
            'stream',
            {
                'name': 'stdout',
                'text': text,
            }
        )

    def _find_stack_items(self, operations: MichelineSequence, stack: MichelsonStack) -> Optional[List[MichelsonInstruction]]:
        for operation in operations.items[::-1]:
            items = getattr(operation, 'items', None)
            if isinstance(items, MichelineSequence):
                stack_items = self._find_stack_items(operations, stack)
                if stack_items:
                    return stack_items
            if not isinstance(operation, MichelsonInstruction):
                continue
            if operation.stack_items_added:
                return stack.items[-operation.stack_items_added:]
        return None

    def _find_lazy_diff(self, operations: MichelineSequence) -> Optional[List[Dict[str, str]]]:
        for operation in operations.items[::-1]:
            if isinstance(operation, CommitInstruction) and operation.lazy_diff:
                return operation.lazy_diff

    def _send_success_response(self, operations: MichelineSequence, stack: MichelsonStack) -> Dict[str, Any]:
        plain, html = '', ''

        modified_items = self._find_stack_items(operations, stack)
        if modified_items:
            table = preformat_stack_table(modified_items)
            plain += plain_table(table)
            html += html_table(table)

        lazy_diff = self._find_lazy_diff(operations)
        if lazy_diff:
            plain += plain_table(lazy_diff)
            html += html_table(lazy_diff)

        result = {
                'data': {
                'text/plain': plain,
                'text/html': html
            },
            'metadata': {},
            'execution_count': self.execution_count,
        }

        self.send_response(
            self.iopub_socket,
            'execute_result',
            result,
        )
        return result

    def _send_fail_response(self, error: Exception) -> Dict[str, Any]:
        if isinstance(error, (MichelsonParserError, MichelsonRuntimeError)):
            traceback = [error.format_stdout()]
        else:
            traceback = format_exception(error.__class__, error, None)
        result = {
            'status': 'error',
            'ename': error.__class__.__name__,
            'evalue': str(error),
            'traceback': traceback,
        }
        self.send_response(
            self.iopub_socket,
            'stream',
            {
                'name': 'stderr',
                'text': '\n'.join(traceback),
            }
        )
        return result

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):

        interpreter_result = self.interpreter.execute(code)

        if not silent and interpreter_result.stdout:
            self._stdout('\n'.join(interpreter_result.stdout))

        if not interpreter_result.error:
            if not silent:
                return self._send_success_response(interpreter_result.operations, interpreter_result.stack)
        else:
            return self._send_fail_response(interpreter_result.error)
        return {}

    def do_complete(self, code, cursor_pos):
        token, begin_pos, end_pos = parse_token(code, cursor_pos)

        suggests = []
        for word_set in [prim_tags, static_macros]:
            for word in word_set:
                if word.startswith(token):
                    suggests.append(word)

        if suggests:
            res = {
                'matches': suggests,
                'cursor_start': begin_pos,
                'cursor_end': end_pos,
            }
        else:
            res = {'matches': [], 'cursor_start': cursor_pos, 'cursor_end': cursor_pos}

        res['status'] = 'ok'
        return res

    def do_inspect(self, code, cursor_pos, detail_level=0):
        token, _, _ = parse_token(code, cursor_pos)
        docstring = docs.get(token)
        if docstring:
            res = {'found': True, 'data': {'text/plain': docstring}}
        else:
            res = {'found': False}

        res['status'] = 'ok'
        return res
