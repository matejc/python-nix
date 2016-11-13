from BTrees.OOBTree import OOBTree
from persistent import Persistent
from uuid import uuid4
from nix.lib.misc import json2nix

import json


class Profiles(Persistent):
    def __init__(self):
        self.profiles = OOBTree()

    def add_profile(self, profile):
        profile.__parent__ = self
        self.profiles[profile._uuid] = profile

    def remove_profile(self, profile_uuid):
        del self.profiles[profile_uuid]


class Profile(Persistent):
    __parent__ = None
    _uuid = None
    _name = None
    _nixpkgs = None
    _build_path = ['scripts']
    _build_script = 'default.nix'
    _nix = {}

    def __init__(self, name):
        self._name = name
        self._uuid = str(uuid4())

    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def nixpkgs(self):
        return self._nixpkgs

    @nixpkgs.setter
    def nixpkgs(self, value):
        self._nixpkgs = value

    @property
    def build_path(self):
        return self._build_path

    @build_path.setter
    def build_path(self, value):
        self._build_path = value

    @property
    def build_script(self):
        return self._build_script

    @build_script.setter
    def build_script(self, value):
        self._build_script = value

    def _recurse_options(self, path, root):
        if len(path) == 0:
            return root
        elif path[0] not in root:
            return None
        else:
            return self._recurse_options(path[1:], root[path[0]])

    def get_option(self, path=[], return_type='dict'):
        native = self._recurse_options(path, self._nix)
        if return_type == 'dict':
            return native
        elif return_type == 'json':
            return json.dumps(native)
        elif return_type == 'nix':
            return json2nix(json.dumps(native))

    def _recurse_set_options(self, path, value, root):
        if len(path) == 1:
            root[path[0]] = value
            return True
        elif path[0] not in root:
            root[path[0]] = {}
            return self._recurse_set_options(path[1:], value, root[path[0]])
        else:
            return self._recurse_set_options(path[1:], value, root[path[0]])

    def set_option(self, path, value):
        res = self._recurse_set_options(path, value, self._nix)
        if res:
            self._p_changed = True
        return res


def appmaker(zodb_root):
    if 'profiles' not in zodb_root:
        profiles = Profiles()
        zodb_root['profiles'] = profiles
        import transaction
        transaction.commit()
    return zodb_root['profiles']
