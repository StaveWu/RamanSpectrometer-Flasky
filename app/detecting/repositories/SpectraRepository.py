from ... import db
from datetime import datetime
from ..models import Spectrum
import numpy as np
import os
from typing import List, Optional


class SpectrumDAO(db.Model):
    __tablename__ = 'spectrum_infos'
    id = db.Column(db.Integer, primary_key=True)  # default auto increment
    name = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class SpectrumComponentsDAO(db.Model):
    __tablename__ = 'spectrum_components'
    spec_id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, primary_key=True)


class SpectrumIO:
    path = ''

    @staticmethod
    def write(id, data):
        pathname = os.path.join(SpectrumIO.path, id)
        with open(pathname, 'w') as f:
            for row_eles in data:
                for i, col_ele in enumerate(row_eles):
                    f.write('%f' % col_ele)
                    if i < len(row_eles) - 1:
                        f.write('\t')
                f.write('\n')

    @staticmethod
    def read_by_id(id):
        pathname = os.path.join(SpectrumIO.path, id)
        data = []
        with open(pathname, 'r') as f:
            for line in f.readlines():
                s = line.strip().split('\t')
                data.append([float(ele) for ele in s])
        return np.array(data).astype('float')


def save_spectrum(spec: Spectrum):
    spec_dao = SpectrumDAO(id=spec.id, name=spec.name)
    db.session.add(spec_dao)
    db.session.commit()

    if len(spec.component_ids) > 0:
        for comp_id in spec.component_ids:
            spec_comps_dao = SpectrumComponentsDAO(spec_id=spec.id, comp_id=comp_id)
            db.session.add(spec_comps_dao)
        db.session.commit()

    SpectrumIO.write(spec.id, spec.data)


def find_by_id(id) -> Optional[Spectrum]:
    spec_dao = db.session.query(SpectrumDAO).filter(SpectrumDAO.id == id).first()
    if not spec_dao:
        return None
    comp_ids = db.session.query(SpectrumComponentsDAO.comp_id).filter(SpectrumComponentsDAO.spec_id == id).all()
    data = SpectrumIO.read_by_id(spec_dao.id)
    spec = Spectrum(id=spec_dao.id, name=spec_dao.name, data=data, component_ids=comp_ids)
    return spec


def find_by_timestamp_desc(limit) -> List[Spectrum]:
    spec_daos = db.session.query(SpectrumDAO).order_by(SpectrumDAO.timestamp.desc()).limit(limit).all()
    res = []
    for spec_dao in spec_daos:
        comp_ids = db.session.query(SpectrumComponentsDAO.comp_id)\
            .filter(SpectrumComponentsDAO.spec_id == spec_dao.id).all()
        data = SpectrumIO.read_by_id(spec_dao.id)
        res.append(Spectrum(id=spec_dao.id, name=spec_dao.name, data=data, component_ids=comp_ids))
    return res


def find_all():
    spec_daos = db.session.query(SpectrumDAO).all()
    res = []
    for spec_dao in spec_daos:
        comp_ids = db.session.query(SpectrumComponentsDAO.comp_id) \
            .filter(SpectrumComponentsDAO.spec_id == spec_dao.id).all()
        data = SpectrumIO.read_by_id(spec_dao.id)
        res.append(Spectrum(id=spec_dao.id, name=spec_dao.name, data=data, component_ids=comp_ids))
    return res
