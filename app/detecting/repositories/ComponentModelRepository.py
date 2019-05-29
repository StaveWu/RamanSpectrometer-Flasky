from ..models.detecting import ComponentModel
from ... import model_io, db
from .daos import ModelDAO


def find_by_id(id):
    dao = db.session.query(ModelDAO).filter(ModelDAO.id == id).one()
    model = model_io.read(id)
    return ComponentModel(id, model, state=dao.state)


def save_model(model: ComponentModel):
    model_io.save(model.delegate)
    dao = ModelDAO(id=model.comp_id, state=model.state)
    db.session.add(dao)
    db.session.commit()


def delete_by_id(id):
    model_io.delete(id)
    ModelDAO.query.filter(ModelDAO.id == id).delete()
    db.session.commit()


def lightweight_find_all():
    """
    find model without delegate, this method is used for whom
    just want to know some information about model instead of
    using them to predict or fit.
    """
    daos = ModelDAO.query.all()
    return [ComponentModel(dao.id, None, dao.state) for dao in daos]
