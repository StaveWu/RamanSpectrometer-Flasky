from ..exceptions import IncompleteFieldError


def get_property(data, prop_name: str):
    prop = data.get(prop_name)
    if prop is None or prop == '':
        raise IncompleteFieldError('{} not found'.format(prop_name))
    return prop

