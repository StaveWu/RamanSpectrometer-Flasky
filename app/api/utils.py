from ..exceptions import PropertyNotFoundError


def get_property(data, prop_name: str):
    prop = data.get(prop_name)
    if prop is None or prop == '':
        raise PropertyNotFoundError('{} not found'.format(prop_name))
    return prop

