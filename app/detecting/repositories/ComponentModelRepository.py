from ..models.detecting import ComponentModel
from ... import model_io
from typing import List


model_caches: List[ComponentModel] = []


def _query_model_in_caches(id):
    for model in model_caches:
        if model.comp_id == id:
            return model
    return None


def find_by_id(id):
    model = _query_model_in_caches(id)
    if not model:
        delegate = model_io.read(id)
        model = ComponentModel(id, delegate)
        model_caches.append(model)
    return model


def save_model(model: ComponentModel):
    model_io.write(model.comp_id, model.delegate)


def delete_by_id(id):
    model_io.delete(id)
    model = _query_model_in_caches(id)
    if model:
        model_caches.remove(model)


