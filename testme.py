from nix.lib.misc import json2nix


print(json2nix('''
{"abc": "1"}
'''))
