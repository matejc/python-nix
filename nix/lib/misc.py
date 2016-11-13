from .run import nixInstantiate

import json


def json2nix(json_string):
    nix_string = '''
    let
      json = ''{}'';
    in builtins.fromJSON json
    '''.format(json_string)

    res = nixInstantiate(['--eval', '--strict', '--show-trace', '-E', '-'],
                         nix_string)
    if res[0] != 0:
        raise Exception("json2nix exited with non-zero exitcode")

    return '\n'.join(res[1])
