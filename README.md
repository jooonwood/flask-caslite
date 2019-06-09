# Flask-CasLite

cas client


## Install


```

pip install Flask-CasLite

```


## Example

```python

from flask import Flask, session, request
from flask_caslite import CasLite, login_required, handle_logout



app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'hello',
    CAS_SERVER = 'https://sso.atbyd.com/cas',
    CAS_VERSION = 'v2',
    CAS_TOKEN_SESSION_KEY = '_CAS_TOKEN',
    CAS_USERNAME_SESSION_KEY = 'CAS_USERNAME',
    CAS_ATTRIBUTES_SESSION_KEY = 'CAS_ATTRIBUTES'
)

CasLite(app)


@app.before_request
def handle_cas_logout():
    print(handle_logout(request))


@app.route('/', methods=['GET'])
def index():
    session['hello'] ='world'
    return 'Hello, World'

@app.route('/private_page/', methods=['GET'])
@login_required
def cas():
    cas_user =session.get('CAS_USERNAME')
    return 'Hello, ' + cas_user + session.get('hello','')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

```