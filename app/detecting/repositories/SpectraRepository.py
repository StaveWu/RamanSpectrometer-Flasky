from ... import db
from ..models import Spectrum
from .io import spectrum_io
from typing import List, Optional
from .daos import SpectrumDAO, SpectrumComponentsDAO


def save_spectrum(spec: Spectrum):
    spec_dao = SpectrumDAO(id=spec.id, name=spec.name)
    db.session.add(spec_dao)
    db.session.commit()

    if len(spec.component_ids) > 0:
        for comp_id in spec.component_ids:
            spec_comps_dao = SpectrumComponentsDAO(spec_id=spec.id, comp_id=comp_id)
            db.session.add(spec_comps_dao)
        db.session.commit()

    spectrum_io.write(spec.id, spec.data)


def find_by_id(id) -> Optional[Spectrum]:
    spec_dao = db.session.query(SpectrumDAO).filter(SpectrumDAO.id == id).first()
    if not spec_dao:
        return None
    comp_ids = db.session.query(SpectrumComponentsDAO.comp_id).filter(SpectrumComponentsDAO.spec_id == id).all()
    data = spectrum_io.read_by_id(spec_dao.id)
    spec = Spectrum(id=spec_dao.id, name=spec_dao.name, data=data, component_ids=comp_ids)
    return spec


def find_by_timestamp_desc(limit) -> List[Spectrum]:
    spec_daos = db.session.query(SpectrumDAO).order_by(SpectrumDAO.timestamp.desc()).limit(limit).all()
    res = []
    for spec_dao in spec_daos:
        comp_ids = db.session.query(SpectrumComponentsDAO.comp_id)\
            .filter(SpectrumComponentsDAO.spec_id == spec_dao.id).all()
        data = spectrum_io.read_by_id(spec_dao.id)
        res.append(Spectrum(id=spec_dao.id, name=spec_dao.name, data=data, component_ids=comp_ids))
    return res


def find_all():
    spec_daos = db.session.query(SpectrumDAO).all()
    res = []
    for spec_dao in spec_daos:
        comp_ids = db.session.query(SpectrumComponentsDAO.comp_id) \
            .filter(SpectrumComponentsDAO.spec_id == spec_dao.id).all()
        data = spectrum_io.read_by_id(spec_dao.id)
        res.append(Spectrum(id=spec_dao.id, name=spec_dao.name, data=data, component_ids=comp_ids))
    return res
