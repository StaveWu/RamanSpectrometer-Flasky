from ..models.detecting import ComponentModel
from ...algorithms.detect import TransferredModel
import os

basedir = ''


def find_by_id(id):
    path = os.path.join(basedir, id)
    if not os.path.exists(path):
        raise FileNotFoundError()
    model = TransferredModel.load(path)
    return ComponentModel(id, model)


def save_model(model):
    path = os.path.join(basedir, model.id)
    if os.path.exists(path):
        print('WARNING: file will be replaced')
    model.delegate.save(path)


def delete_by_id(id):
    path = os.path.join(basedir, id)
    if os.path.exists(path):
        os.remove(path)

