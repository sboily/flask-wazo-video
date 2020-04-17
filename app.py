import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort, jsonify
from wazo_auth_client import Client


load_dotenv()
wazo_server = os.environ.get('WAZO_SERVER')
wazo_username = os.environ.get('WAZO_USERNAME')
wazo_password = os.environ.get('WAZO_PASSWORD')
wazo_room = os.environ.get('WAZO_ROOM')

app = Flask(__name__)
client = Client(wazo_server, username=wazo_username, password=wazo_password)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.get_json(force=True).get('username')
    if not username:
        abort(401)
    session = client.token.new('wazo_user', expiration=3600)
    session['uuid'] = session['metadata']['user_uuid']

    return jsonify({'host': wazo_server, 'session': session, 'room': wazo_room})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
