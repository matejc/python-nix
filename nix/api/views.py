from pyramid.view import view_config
from .models import Profiles
from .models import Profile


@view_config(route_name='api.things.get', context='.models.Profiles')
def get_things(context, request):
    p = Profile('beje')
    p.set_option(['a'], 12)
    p.set_option(['b'], [1, 2, 3])
    p.set_option(['c'], {"a": {"b": {"c": 123}}})
    p.set_option(['c', 'a'], {"c": 123})
    context.add_profile(p)

    a = context.profiles[p.uuid]

    return {"dict": a.get_option(),
            "uuid": a.uuid,
            "name": a.name,
            "nix": a.get_option(return_type='nix')}
