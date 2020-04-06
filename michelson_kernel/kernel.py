from tabulate import tabulate
from ipykernel.kernelbase import Kernel

from pytezos.repl.helpers import helpers_prim
from pytezos.michelson.macros import primitives
from pytezos.repl.interpreter import Interpreter

from michelson_kernel import __version__
from michelson_kernel.docs import docs

static_macros = [
    'CMPEQ', 'CMPNEQ', 'CMPLT', 'CMPGT', 'CMPLE', 'CMPGE',
    'IFEQ', 'IFNEQ', 'IFLT', 'IFGT', 'IFLE', 'IFGE',
    'IFCMPEQ', 'IFCMPNEQ', 'IFCMPLT', 'IFCMPGT', 'IFCMPLE', 'IFCMPGE',
    'FAIL',
    'ASSERT_EQ', 'ASSERT_NEQ', 'ASSERT_LT', 'ASSERT_GT', 'ASSERT_LE', 'ASSERT_GE',
    'ASSERT_CMPEQ', 'ASSERT_CMPNEQ', 'ASSERT_CMPLT', 'ASSERT_CMPGT', 'ASSERT_CMPLE', 'ASSERT_CMPGE',
    'ASSERT_NONE', 'ASSERT_SOME', 'ASSERT_LEFT', 'ASSERT_RIGHT',
    'UNPAIR',
    'IF_SOME',
    'SET_CAR', 'SET_CDR',
    'MAP_CAR', 'MAP_CDR'
]


def parse_token(line, cursor_pos):
    begin_pos = next((i + 1 for i in range(cursor_pos - 1, 0, -1) if line[i] in ' ;({\n'), 0)
    end_pos = next((i for i in range(cursor_pos, len(line)) if line[i] in ' ;){\n'), len(line))
    return line[begin_pos:end_pos], begin_pos, end_pos


def html_table(items):
    def pre(s):
        return f'<pre style="text-align: left;">{s}</pre>'

    def pre_dict(d):
        return {k: pre(v) for k, v in d.items()}

    res = tabulate(list(map(pre_dict, items)), tablefmt='html', headers="keys")
    res = res.replace('&lt;', '<').replace('&gt;', '>')  # tabulate escapes our <pre> tags
    return res


def plain_table(items):
    return tabulate(items, tablefmt='simple', headers="keys")


def format_result(result, execution_count):
    kind = result['kind']
    if kind in ['message', 'code']:
        plain, html = result['value'], result['value']
    elif kind in ['stack', 'big_map_diff']:
        plain = plain_table(result['value'])
        html = html_table(result['value'])
    elif kind == 'output':
        ops, storage, bmd = result['value']
        data = list(filter(lambda x: len(x) > 0, [storage, bmd, ops]))
        plain = '\n'.join(map(plain_table, data))
        html = '<br>'.join(map(html_table, data))
    else:
        assert False, kind
    return {'data': {'text/plain': plain,
                     'text/html': html},
            'metadata': {},
            'execution_count': execution_count}


class MichelsonKernel(Kernel):
    implementation = 'IMichelson'
    implementation_version = __version__
    language_info = {
        'name': 'Michelson',
        'mimetype': 'text/x-michelson',
        'file_extension': '.tz',
        'codemirror_mode': 'michelson'
    }
    banner = 'Michelson (Tezos VM language)'
    help_links = [
        'https://michelson.nomadic-labs.com/',
        'https://tezos.gitlab.io/whitedoc/michelson.html'
    ]

    def __init__(self, **kwargs):
        super(MichelsonKernel, self).__init__(**kwargs)
        self.interpreter = Interpreter(debug=False)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        int_res = self.interpreter.execute(code)
        if not silent and int_res.get('stdout'):
            self.send_response(
                self.iopub_socket, 'stream', {'name': 'stdout',
                                              'text': int_res['stdout']})

        if int_res.get('success'):
            res = {'status': 'ok'}
            if not silent and int_res.get('result'):
                self.send_response(
                    self.iopub_socket, 'execute_result', format_result(int_res['result'], self.execution_count))
        else:
            res = {'status': 'error'}
            if int_res.get('stderr'):
                traceback = [f'{int_res["stderr"]["name"]}: {int_res["stderr"]["value"]}',
                             int_res["stderr"]["trace"]]
                res = {'ename': int_res['stderr']['name'],
                       'evalue': int_res['stderr']['value'],
                       'traceback': traceback}
                self.send_response(
                    self.iopub_socket, 'stream', {'name': 'stderr',
                                                  'text': '\n'.join(traceback)})

        res['execution_count'] = self.execution_count
        return res

    def do_complete(self, code, cursor_pos):
        token, begin_pos, end_pos = parse_token(code, cursor_pos)

        suggests = []
        for word_set in [primitives, static_macros, helpers_prim]:
            for word in word_set:
                if word.startswith(token):
                    suggests.append(word)

        if suggests:
            res = {
                'matches': suggests,
                'cursor_start': begin_pos,
                'cursor_end': end_pos}
        else:
            res = {
                'matches': [],
                'cursor_start': cursor_pos,
                'cursor_end': cursor_pos}

        res['status'] = 'ok'
        return res

    def do_inspect(self, code, cursor_pos, detail_level=0):
        token, _, _ = parse_token(code, cursor_pos)
        docstring = docs.get(token)
        if docstring:
            res = {
                'found': True,
                'data': {'text/plain': docstring}}
        else:
            res = {'found': False}

        res['status'] = 'ok'
        return res
