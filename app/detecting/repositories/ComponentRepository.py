from ... import db
from ..models import Component, SpectrumBase
from .io import component_io
from typing import Optional


class ComponentDAO(db.Model):
    __tablename__ = 'component_infos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    formula = db.Column(db.Text, nullable=True)


class ComponentSpectraDAO(db.Model):
    __tablename__ = 'component_spectra'
    spec_id = db.Column(db.Integer, primary_key=True)
    spec_name = db.Column(db.Text)
    comp_id = db.Column(db.Integer)  # corresponding to ComponentDAO id


def save_component(comp: Component):
    comp_dao = ComponentDAO(id=comp.id, name=comp.name, formula=comp.formula)
    db.session.add(comp_dao)
    db.session.commit()

    for cos in comp.owned_spectra:
        comp_spec_dao = ComponentSpectraDAO(spec_name=cos.name, comp_id=comp.id)
        db.session.add(comp_spec_dao)
        db.session.commit()
        component_io.write(comp_spec_dao.id, cos.data)


def find_by_id(id) -> Optional[Component]:
    comp_dao = db.session.query(ComponentDAO).filter(ComponentDAO.id == id).first()
    if not comp_dao:
        return None
    comp_spec_daos = db.session.query(ComponentSpectraDAO)\
        .filter(ComponentSpectraDAO.comp_id == comp_dao.id).all()
    owned_spectra = []
    for dao in comp_spec_daos:
        data = component_io.read_by_id(dao.spec_id)
        owned_spectra.append(SpectrumBase(id=dao.id, name=dao.name, data=data))
    return Component(id=comp_dao.id, name=comp_dao.name,
                     owned_spectra=owned_spectra, formula=comp_dao.formula)


def find_all():
    comp_daos = db.session.query(ComponentDAO).all()
    res = []
    for comp_dao in comp_daos:
        comp_spec_daos = db.session.query(ComponentSpectraDAO)\
            .filter(ComponentSpectraDAO.comp_id == comp_dao.id).all()
        owned_spectra = []
        for dao in comp_spec_daos:
            data = component_io.read_by_id(dao.spec_id)
            owned_spectra.append(SpectrumBase(id=dao.id, name=dao.name, data=data))
        res.append(Component(id=comp_dao.id, name=comp_dao.name,
                             owned_spectra=owned_spectra, formula=comp_dao.formula))
    return res


def delete_by_id(id):
    comp_spec_daos = ComponentSpectraDAO.query.filter(ComponentSpectraDAO.comp_id == id).all()
    for dao in comp_spec_daos:
        component_io.delete_by_id(dao.spec_id)
    ComponentSpectraDAO.query.filter(ComponentSpectraDAO.comp_id == id).delete()
    ComponentDAO.query.filter(ComponentDAO.id == id).delete()
    db.session.commit()


