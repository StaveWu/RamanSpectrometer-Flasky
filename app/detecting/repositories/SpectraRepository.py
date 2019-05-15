from ... import db
from datetime import datetime
from ..models import Spectrum


class SpectraDAO(db.Model):
    __tablename__ = 'spectrum_infos'
    id = db.Column(db.Integer, primary_key=True)  # default auto increment
    name = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


def get_train_data_by_comp_id(comp_id):
    pass


def save_spectrum(spec):
    pass


def find_by_id(id)->Spectrum:
    pass


def find_by_timestamp_desc(limit):
    pass


def find_all():
    pass
