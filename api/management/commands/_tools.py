def _ordering(row: str):
    data = row.split(':')
    if len(data) < 2:
        print('!!!', data)
        return
    return {
        'file': data[0],
        'line': int(data[1]),
        'description': _after_todo(':'.join(data[2:])),
    }


def _after_todo(line: str):
    pat = 'todo: '
    return (lambda s: s[s.index(pat):][len(pat):])(line.replace('TODO', 'todo'))


def _filter_line(line: str):
    if line.startswith('grep: '):
        return False
    if line.startswith('Двоичный файл'):
        return False
    if not line:
        return False
    return True


def pick_todo(result_command: str):
    rows = result_command.split('\n')
    return list(map(_ordering, filter(_filter_line, rows)))
