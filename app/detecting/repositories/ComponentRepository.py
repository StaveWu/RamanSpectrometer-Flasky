from ... import db
from ..models import Component, SpectrumBase
import os
import numpy as np
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


class ComponentIO:
    path = ''

    @staticmethod
    def write(id, data):
        pathname = os.path.join(ComponentIO.path, id)
        with open(pathname, 'w') as f:
            for row_eles in data:
                for i, col_ele in enumerate(row_eles):
                    f.write('%f' % col_ele)
                    if i < len(row_eles) - 1:
                        f.write('\t')
                f.write('\n')

    @staticmethod
    def read_by_id(id):
        pathname = os.path.join(ComponentIO.path, id)
        data = []
        with open(pathname, 'r') as f:
            for line in f.readlines():
                s = line.strip().split('\t')
                data.append([float(ele) for ele in s])
        return np.array(data).astype('float')

    @staticmethod
    def delete_by_id(id):
        pathname = os.path.join(ComponentIO.path, id)
        if os.path.exists(pathname):
            os.remove(pathname)


def save_component(comp: Component):
    comp_dao = ComponentDAO(id=comp.id, name=comp.name, formula=comp.formula)
    db.session.add(comp_dao)
    db.session.commit()

    for cos in comp.owned_spectra:
        comp_spec_dao = ComponentSpectraDAO(spec_name=cos.name, comp_id=comp.id)
        db.session.add(comp_spec_dao)
        db.session.commit()
        ComponentIO.write(comp_spec_dao.id, cos.data)


def find_by_id(id) -> Optional[Component]:
    comp_dao = db.session.query(ComponentDAO).filter(ComponentDAO.id == id).first()
    if not comp_dao:
        return None
    comp_spec_daos = db.session.query(ComponentSpectraDAO)\
        .filter(ComponentSpectraDAO.comp_id == comp_dao.id).all()
    owned_spectra = []
    for dao in comp_spec_daos:
        data = ComponentIO.read_by_id(dao.spec_id)
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
            data = ComponentIO.read_by_id(dao.spec_id)
            owned_spectra.append(SpectrumBase(id=dao.id, name=dao.name, data=data))
        res.append(Component(id=comp_dao.id, name=comp_dao.name,
                             owned_spectra=owned_spectra, formula=comp_dao.formula))
    return res


def delete_by_id(id):
    comp_spec_daos = ComponentSpectraDAO.query.filter(ComponentSpectraDAO.comp_id == id).all()
    for dao in comp_spec_daos:
        ComponentIO.delete_by_id(dao.spec_id)
    ComponentSpectraDAO.query.filter(ComponentSpectraDAO.comp_id == id).delete()
    ComponentDAO.query.filter(ComponentDAO.id == id).delete()
    db.session.commit()


