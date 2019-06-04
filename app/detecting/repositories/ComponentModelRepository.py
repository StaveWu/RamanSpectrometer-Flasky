from ..models.detecting import ComponentModel
from ... import model_io


def find_by_id(id):
    model = model_io.read(id)
    return ComponentModel(id, model)


def save_model(model: ComponentModel):
    model_io.write(model.comp_id, model.delegate)


def delete_by_id(id):
    model_io.delete(id)

