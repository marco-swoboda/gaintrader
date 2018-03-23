'''
Backaend for Algo Trading bot
'''
import os
import uuid
import datetime as dt
from functools import wraps
import click
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'gaintrader.db')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
print(app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    '''
    A User
    '''
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    token = db.Column(db.String(120))
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    value = db.Column(db.String(250))

@app.cli.command('createuser')
@click.option('--username', help="Enter the username.")
@click.option('--password', prompt=True, hide_input=True, help="Enter the user's password.")
def create_user_cli(username, password):
    """Creates a new admin user."""
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User.query.filter_by(name=username).first()
    if not new_user:
        new_user = User(public_id=str(uuid.uuid4()), name=username, password=hashed_password, token=None, admin=True)
        db.session.add(new_user)
        print('Creating user', username, 'with password', password, '.')
    else:
        new_user.password = hashed_password
        new_user.admin = True
        print('Replacing user', username, 'with password', password, '.')
    db.session.commit()

@app.cli.command('reset_jwt_secret')
def reset_token_secret():
    """Recreate a new secret for the session tokens"""
    secret = Config.query.filter_by(key="JWT_SECRET_KEY").first()
    new_secret = str(uuid.uuid4())
    if secret:
        print("Old secret:", secret.value, "New secret:", new_secret)
        secret.value = new_secret
    else:
        print("New secret:", new_secret)
        secret = Config(key="JWT_SECRET_KEY", value=new_secret)
        db.session.add(secret)
    app.config['JWT_SECRET_KEY'] = new_secret
    db.session.commit()

def load_jwt_secret():
    secret = Config.query.filter_by(key="JWT_SECRET_KEY").first()
    if secret:
        app.config['JWT_SECRET_KEY'] = secret.value
        print("Secret loaded:", secret.value)
    else:
        reset_token_secret()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Login required.'}), 401

        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Login required.'}), 401
        
        if not current_user or not token == current_user.token:
            return jsonify({'message': 'Login required.'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/user', methods=['GET'])
@login_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['token'] = user.token
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({"users" : output})

@app.route('/user/<public_id>', methods=['GET'])
@login_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message" : "User does not exist."}), 404

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['token'] = user.token
    user_data['admin'] = user.admin

    return jsonify({"user": user_data})

@app.route('/user', methods=['POST'])
@login_required
def create_user(current_user):
    data = request.get_json()
    print(data)
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, token=None, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created.'})

@app.route('/user/<public_id>', methods=['PUT'])
@login_required
def promote_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "User does not exist."}), 404

    user.admin = True
    db.session.commit()

    return jsonify({"message": "User has been promoted!"})

@app.route('/user/<public_id>', methods=['DELETE'])
@login_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "User does not exist."}), 404
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User has been deleted!"})

@app.route('/login')
def login():
    credentials = request.get_json()
    
    if not credentials or not credentials.username or not credentials.password:
        return jsonify({"message": "Login failed."}), 401
    
    user = User.query.filter_by(name=credentials.username).first()

    if not user:
        return jsonify({"message": "Login failed."}), 401

    if not check_password_hash(user.password, credentials.password):
        return jsonify({"message": "Login failed."}), 401

    token = jwt.encode({'public_id': user.public_id, 'exp' : dt.datetime.utcnow() + dt.timedelta(minutes=60)}, app.config['JWT_SECRET_KEY'])
    user.token = token
    db.session.commit()

    return jsonify({'token': token.decode('UTF-8')})

load_jwt_secret()

if __name__ == '__main__':
    app.run()