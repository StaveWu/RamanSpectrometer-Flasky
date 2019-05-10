from . import db
from datetime import datetime
from .exceptions import ValidationError


class Spectra(db.Model):
    __tablename__ = 'spectras'
    id = db.Column(db.Integer, primary_key=True)  # default auto increment
    name = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def from_json(json_spectra):
        name = json_spectra.get('name')
        data = json_spectra.get('data')
        if name is None or name == '':
            raise ValidationError('post does not have a name')
        if data is None or data == '':
            raise ValidationError('post does not have a data')

        # save data to file

        # save name to db
        return Spectra(name=name)

    def to_json(self):
        json_spectra = {
            'id': self.id,
            'name': self.name,
            'data': 'load data from file'
        }
        return json_spectra
