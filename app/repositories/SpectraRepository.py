from .. import db
from datetime import datetime


class SpectraDAO(db.Model):
    __tablename__ = 'spectras'
    id = db.Column(db.Integer, primary_key=True)  # default auto increment
    name = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


def get_train_data_by_comp_id(comp_id):
    pass


def save_spectra(spec):
    pass


def find_spectra_by_id(id):
    pass


def find_spectra_order_by_timestamp(limit: int):
    pass
