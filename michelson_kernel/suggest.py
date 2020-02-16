from pytezos.michelson.macros import primitives

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
    begin_pos = next((i + 1 for i in range(cursor_pos - 1, 0, -1) if line[i] in {' ', ';', '(', '{'}), 0)
    end_pos = next((i for i in range(cursor_pos, len(line)) if line[i] in {' ', ';', ')', '{'}), len(line))
    return line[begin_pos:end_pos], begin_pos, end_pos


def get_suggests(token):
    suggests = []
    for word_set in [primitives, static_macros]:
        for word in word_set:
            if word.startswith(token):
                suggests.append(word)
    return suggests
