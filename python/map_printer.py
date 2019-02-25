    
class bcolors:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_state(state, N, M):
    _print_map(_make_map(state, N, M))


def _make_map(state, N, M):
    _map = []
    for _ in range(N):
        _map.append(['.'] * M)
    for entity in state:
        prefix = None
        if entity['type'] == 'W':
            prefix = bcolors.YELLOW
        if entity['type'] == 'V':
            prefix = bcolors.RED
        _map[entity['x']][entity['y']] = prefix + str(entity['number']) + \
            bcolors.DEFAULT if prefix else str(entity['number'])
    return _map


def _print_map(_map):
    printable_map = []
    for line in _map:
        printable_map.append(''.join(line))
    print('\n'.join(printable_map))
