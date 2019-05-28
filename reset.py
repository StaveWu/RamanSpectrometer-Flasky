from flasky import app
from app import db
from shutil import rmtree
import os

# recreate db
with app.app_context() as ctx:
    db.drop_all()
    db.create_all()


# recreate path
def recreate_path(path):
    if os.path.exists(path):
        rmtree(path)
    os.mkdir(path)


model_path = app.config['MODEL_PATH']
spectra_path = app.config['SPECTRA_PATH']
component_path = app.config['COMPONENT_PATH']

recreate_path(model_path)
recreate_path(spectra_path)
recreate_path(component_path)
