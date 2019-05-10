from flask import Flask, url_for

app = Flask(__name__)


@app.route('/login')
def login():
    pass


with app.test_request_context():
    print(url_for('login', id=2))
