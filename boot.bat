echo FLASK_APP=flasky>.env
echo FLASK_ENV=production>>.env
echo FLASK_CONFIG=production>>.env

python -m venv venv
venv/Scripts/activate.bat
pip install -r requirements/common.txt
python reset.py
