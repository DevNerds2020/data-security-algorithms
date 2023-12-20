from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnerable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()


def insecure_db_execute(query):
    # when a database is not properly configured, it is possible to execute multiple queries at once
    results = []
    statements = [s.strip() for s in query.split(';') if s.strip()]
    for statement in statements:
        result = db.session.execute(db.text(statement))
        results.append(result)
    try:
        db.session.commit()
    except:
        print('Error committing changes to database!')
    return results[0].fetchone()



@app.before_request
def before_request():
    g.roles = ['admin']  # Mock user roles for demonstration purposes

# Broken access control, no proper authorization
@app.route('/users', methods=['GET'])
def get_users():
    if 'admin' in g.roles:
        users = User.query.all()
        return jsonify([{'username': user.username, 'role': user.role, 'id': user.id} for user in users])
    else:
        return jsonify({'error': 'Unauthorized access!'})


@app.route('/change_user_role', methods=['POST'])
def change_user_role():
    if 'admin' in g.roles:  # Broken access control, no proper authorization
        user_id = request.json.get('user_id')
        new_role = request.json.get('new_role')
        print(User.query.all())
        user = User.query.filter_by(id=user_id).first()

        if user:
            user.role = new_role
            db.session.commit()
            return jsonify({'message': 'User role changed successfully!'})
        else:
            return jsonify({'error': 'User not found!'})
    else:
        return jsonify({'error': 'Unauthorized access!'})

# SQL injection 
@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    user_id = request.args.get('user_id')
    query = f"SELECT * FROM User WHERE id = {user_id}"
    user_data = insecure_db_execute(query)

    if user_data:
        return jsonify({'username': user_data.username, 'role': user_data.role, 'id': user_data.id})
    else:
        return jsonify({'error': 'User not found!'})

# safe SQL injection
@app.route('/get_user_data_safe', methods=['GET'])
def get_user_data_safe():
    user_id = request.args.get('user_id')
    query = f"SELECT * FROM User WHERE id = :user_id"
    user_data = db.session.execute(db.text(query), {'user_id': user_id}).fetchone()

    if user_data:
        return jsonify({'username': user_data.username, 'role': user_data.role, 'id': user_data.id})
    else:
        return jsonify({'error': 'User not found!'})

if __name__ == '__main__':
    app.run(debug=True)
