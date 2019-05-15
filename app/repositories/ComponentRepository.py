from .. import db


class ComponentDAO(db.Model):
    __tablename__ = 'component_infos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    formula = db.Column(db.Text, nullable=True)


def save_component(comp):
    pass


def find_by_id(id):
    pass


def find_by_component_id(comp_id):
    pass


def delete_by_name(comp_name):
    pass


def find_by_name(comp_name):
    pass


def find_by_max_component_id():
    pass


def find_all():
    pass


def delete_by_id(id):
    pass
