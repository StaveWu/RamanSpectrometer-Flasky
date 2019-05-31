from ..exceptions import IncompleteFieldError


class JsonWrapper:
    """Value object"""
    def __init__(self, json):
        if not isinstance(json, dict):
            raise ValueError('expect dict but get {}'.format(type(json)))
        self.json = json

    def get_strict(self, key, type=None):
        res = self.json.get(key)
        if res is None or res == '':
            raise IncompleteFieldError('{} not found'.format(key))
        if isinstance(res, dict):
            return JsonWrapper(res)
        elif type:
            return type(res)
        else:
            return res

    def get(self, key):
        res = self.json.get(key)
        return JsonWrapper(res) if isinstance(res, dict) else res



