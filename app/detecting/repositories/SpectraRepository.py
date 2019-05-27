from ... import db, spectrum_io
from ..models import Spectrum
from typing import List
from .daos import SpectrumDAO, SpectrumComponentsDAO


def save_spectrum(spec: Spectrum):
    db.session.add(spec.dao)
    db.session.commit()

    for comp_id in spec.component_ids:
        spec_comps_dao = SpectrumComponentsDAO(spec_id=spec.id, comp_id=comp_id)
        db.session.add(spec_comps_dao)
    db.session.commit()

    spectrum_io.write(spec.id, spec.data)


def find_by_id(id) -> Spectrum:
    spec_dao = db.session.query(SpectrumDAO).filter(SpectrumDAO.id == id).one()
    comp_ids = db.session.query(SpectrumComponentsDAO.comp_id).filter(SpectrumComponentsDAO.spec_id == id).all()
    data = spectrum_io.read(spec_dao.id)
    return Spectrum.of(spec_dao, data, comp_ids)


def find_by_timestamp_desc(limit) -> List[Spectrum]:
    spec_daos = db.session.query(SpectrumDAO).order_by(SpectrumDAO.timestamp.desc()).limit(limit).all()
    res = []
    for spec_dao in spec_daos:
        comp_ids = db.session.query(SpectrumComponentsDAO.comp_id)\
            .filter(SpectrumComponentsDAO.spec_id == spec_dao.id).all()
        data = spectrum_io.read(spec_dao.id)
        res.append(Spectrum.of(spec_dao, data, comp_ids))
    return res


def find_all():
    spec_daos = db.session.query(SpectrumDAO).all()
    res = []
    for spec_dao in spec_daos:
        comp_ids = db.session.query(SpectrumComponentsDAO.comp_id) \
            .filter(SpectrumComponentsDAO.spec_id == spec_dao.id).all()
        data = spectrum_io.read(spec_dao.id)
        res.append(Spectrum.of(spec_dao, data, comp_ids))
    return res
