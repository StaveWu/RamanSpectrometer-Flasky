from ... import db
from .daos import ModelDAO
from ..models import ModelState


def find_by_id(id):
    dao = db.session.query(ModelDAO).filter(ModelDAO.id == id).one()
    return ModelState.of(id, dao.state)


def find_all():
    daos = ModelDAO.query.all()
    return [ModelState.of(dao.id, dao.state) for dao in daos]


def save_state(state: ModelState):
    dao = ModelDAO(id=state.comp_id, state=state.state.value)
    db.session.add(dao)
    db.session.commit()


def delete_by_id(id):
    ModelDAO.query.filter(ModelDAO.id == id).delete()
    db.session.commit()


def update_state(state: ModelState):
    dao = db.session.query(ModelDAO).filter(ModelDAO.id == state.comp_id).one()
    dao.state = state.state.value
    db.session.commit()
