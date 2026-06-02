from flask import Flask, request, jsonify
from models import db, ma, Credential
from security import encrypt_string, decrypt_string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cofre.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)

# User model for demonstration purposes (assuming it's already defined elsewhere)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

@app.route('/credentials', methods=['POST'])
@app.route('/credentials', methods=['GET'])
def list_credentials():
    user_id = request.args.get('user_id')
    credentials = Credential.query.filter_by(user_id=user_id).all()
    schema = CredentialSchema(many=True)
    result = schema.dump(credentials)
    return jsonify(result)

@app.route('/credentials/<int:id>', methods=['PUT'])
@app.route('/credentials/<int:id>', methods=['DELETE'])
def delete_credential(id):
    user_id = request.args.get('user_id')
    credential = Credential.query.get_or_404(id)
    if credential.user_id != user_id:
        return jsonify({'message': 'Access denied'}), 403

    db.session.delete(credential)
    db.session.commit()

    return jsonify({'message': 'Credential deleted successfully'})

@app.route('/revelar_senha/<int:id>', methods=['POST'])
def reveal_credential(id):
    user_id = request.args.get('user_id')
    data = request.get_json()
    password = data['password']

    credential = Credential.query.get_or_404(id)
    if credential.user_id != user_id:
        return jsonify({'message': 'Access denied'}), 403

    decrypted_password = decrypt_string(credential.encrypted_password)

    if password != decrypt_string(decrypted_password):
        return jsonify({'message': 'Invalid password'}), 401

    return jsonify({'decrypted_password': decrypted_password})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)