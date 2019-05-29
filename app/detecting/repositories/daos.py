from ... import db
from datetime import datetime


class SpectrumDAO(db.Model):
    __tablename__ = 'spectrum_infos'
    id = db.Column(db.Integer, primary_key=True)  # default auto increment
    name = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class SpectrumComponentsDAO(db.Model):
    __tablename__ = 'spectrum_components'
    spec_id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, primary_key=True)


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


class ModelDAO(db.Model):
    __tablename__ = 'model_infos'
    id = db.Column(db.Integer, primary_key=True)  # corresponding to ComponentDAO id
    state = db.Column(db.Text)
