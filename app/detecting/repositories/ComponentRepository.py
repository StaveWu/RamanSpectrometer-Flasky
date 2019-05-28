from ... import db, component_io
from ..models import Component, SpectrumBase
from .daos import ComponentDAO, ComponentSpectraDAO


def save_component(comp: Component):
    db.session.add(comp.dao)
    db.session.commit()

    for cos in comp.owned_spectra:
        comp_spec_dao = ComponentSpectraDAO(spec_name=cos.name, comp_id=comp.id)
        db.session.add(comp_spec_dao)
        db.session.commit()
        component_io.write(comp_spec_dao.spec_id, cos.data)


def find_by_id(id) -> Component:
    comp_dao = db.session.query(ComponentDAO).filter(ComponentDAO.id == id).one()
    comp_spec_daos = db.session.query(ComponentSpectraDAO)\
        .filter(ComponentSpectraDAO.comp_id == comp_dao.id).all()
    owned_spectra = []
    for dao in comp_spec_daos:
        data = component_io.read(dao.spec_id)
        owned_spectra.append(SpectrumBase(name=dao.spec_name, data=data))
    return Component.of(comp_dao, owned_spectra)


def find_all():
    comp_daos = db.session.query(ComponentDAO).all()
    res = []
    for comp_dao in comp_daos:
        comp_spec_daos = db.session.query(ComponentSpectraDAO)\
            .filter(ComponentSpectraDAO.comp_id == comp_dao.id).all()
        owned_spectra = []
        for dao in comp_spec_daos:
            data = component_io.read(dao.spec_id)
            owned_spectra.append(SpectrumBase(name=dao.spec_name, data=data))
        res.append(Component.of(comp_dao, owned_spectra))
    return res


def delete_by_id(id):
    comp_spec_daos = ComponentSpectraDAO.query.filter(ComponentSpectraDAO.comp_id == id).all()
    for dao in comp_spec_daos:
        component_io.delete(dao.spec_id)
    ComponentSpectraDAO.query.filter(ComponentSpectraDAO.comp_id == id).delete()
    ComponentDAO.query.filter(ComponentDAO.id == id).delete()
    db.session.commit()


